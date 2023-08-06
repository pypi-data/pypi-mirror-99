import os

import torch
import torch.optim as optim
from sysflow.utils.common_utils.file_utils import dump, load, make_dir 
import wandb

from neuralsampler.networks import SmallMLP
from neuralsampler.utils import *
from scipy.interpolate import griddata
from tqdm.autonotebook import trange

class neuralsampler: 
    def __init__(self, args, exp_dir, logger): 
        # save the params 
        device = torch.device("cuda:" + str(0) if torch.cuda.is_available() else "cpu")

        #region unpack the params
        niters = args.niters
        batch_size = args.batch_size
        lr = args.lr
        weight_decay = args.weight_decay
        critic_weight_decay = args.critic_weight_decay
        save = args.save
        viz_freq = args.viz_freq
        d_iters = args.d_iters
        g_iters = args.g_iters
        l2 = args.l2
        r = args.r
        sd = args.sd
        n_comp = args.n_comp
        z_dim = args.z_dim
        lr_D = args.lr_D
        out_dim = args.out_dim
        hid_dim = args.hid_dim
        model = args.model
        dim = args.dim
        G_path = args.G_path
        D_path = args.D_path
        use_spectrum = args.use_spectrum
        clip_D = args.clip_D
        clip_value = args.clip_value
        loss_A = args.loss_A
        mmd_ratio_in = args.mmd_ratio_in
        mmd_two_sample = args.mmd_two_sample
        mmd_beta = args.mmd_beta
        G_loss = args.G_loss
        #endregion

        D = SmallMLP(dim, n_hid=hid_dim, n_out=1, UseSpectral=use_spectrum)
        G = SmallMLP(dim, n_hid=hid_dim, n_out=1, UseSpectral=use_spectrum)

        D.to(device)
        G.to(device)

        # load model 
        # pretrained model
        if G_path: 
            G_params = torch.load(G_path)
            G.load_state_dict(G_params)
        if D_path: 
            D_params = torch.load(D_path)
            D.load_state_dict(D_params)

        logger.info(D)
        logger.info(G)

        G_optimizer = optim.Adam(
            G.parameters(), lr=lr, weight_decay=weight_decay, betas=(0.9, 0.999)
        )
        D_optimizer = optim.Adam(
            D.parameters(),
            lr=lr,
            betas=(0.9, 0.999),
            weight_decay=critic_weight_decay,
        )

        #region pack the params
        self.device = device
        self.D = D
        self.G = G
        self.G_optimizer = G_optimizer
        self.D_optimizer = D_optimizer
        self.logger = logger
        self.exp_dir = exp_dir
        self.niters = niters
        self.batch_size = batch_size
        self.lr = lr
        self.weight_decay = weight_decay
        self.critic_weight_decay = critic_weight_decay
        self.save = save
        self.viz_freq = viz_freq
        self.d_iters = d_iters
        self.g_iters = g_iters
        self.l2 = l2
        self.r = r
        self.sd = sd
        self.n_comp = n_comp
        self.z_dim = z_dim
        self.lr_D = lr_D
        self.out_dim = out_dim
        self.hid_dim = hid_dim
        self.model = model
        self.dim = dim
        self.G_path = G_path
        self.D_path = D_path
        self.use_spectrum = use_spectrum
        self.clip_D = clip_D
        self.clip_value = clip_value
        self.loss_A = loss_A
        self.mmd_ratio_in = mmd_ratio_in
        self.mmd_two_sample = mmd_two_sample
        self.mmd_beta = mmd_beta
        self.G_loss = G_loss
        #endregion


    def train(self): 

        #region unpack the params
        niters = self.niters
        batch_size = self.batch_size
        viz_freq = self.viz_freq
        d_iters = self.d_iters
        g_iters = self.g_iters
        l2 = self.l2
        model = self.model
        dim = self.dim
        device = self.device
        D = self.D
        G = self.G
        G_optimizer = self.G_optimizer
        D_optimizer = self.D_optimizer
        exp_dir = self.exp_dir
        clip_D = self.clip_D
        clip_value = self.clip_value
        loss_A = self.loss_A
        mmd_ratio_in = self.mmd_ratio_in
        mmd_two_sample = self.mmd_two_sample
        mmd_beta = self.mmd_beta
        G_loss = self.G_loss
        #endregion

        G.train()
        D.train()


        X_list = []
        Y_list = []
        Z_list = []
        D_list = []

        # get the data via the path (model and dim)
        fname = "{}_d{}.pkl".format(model, dim)
        fname = os.path.join("./dataset/traj", fname)        
        data_dict = load(fname)

        X, Y = data_dict['x'], data_dict['y']

        # trainer the network
        for itr in trange(niters):
            G_optimizer.zero_grad()
            D_optimizer.zero_grad()
            
            #region sample 
            idx = np.random.choice(len(X), batch_size)
            x = X[idx]
            y = Y[idx]
            x = torch.tensor(x, requires_grad=True).float().to(device)
            y = torch.tensor(y, requires_grad=True).float().to(device)

            if mmd_two_sample: 
                idx = np.random.choice(len(X), batch_size)
                x2 = X[idx]
                y2 = Y[idx]
                x2 = torch.tensor(x2, requires_grad=True).float().to(device)
                y2 = torch.tensor(y2, requires_grad=True).float().to(device)
            #endregion

            # 2 gan formulas
            # 2 mmd formula [x8] [combine with the two method] (mmd, mmd_2sample, mmd outside, mmd_2sample outside)

            # loss_A: whether to use the first type of objective
            # ratio_in: whether to put the ratio inside 
            # two_sample: whether to use two pair of samples
            if loss_A:
                # Σ exp(G(xi))/ Z delta_xi, Σ exp(G(xi))/ Z delta_yi
                potential = G(x)
                ratio = torch.exp( potential ) 
                ratio = ratio / ratio.mean()
                D_diff = ratio * ( D(x) - D(y) )
                loss = D_diff.mean()  
                
                if mmd_ratio_in: 
                    # ratio is inside 
                    if mmd_two_sample: 
                        potential2 = G(x2)
                        ratio2 = torch.exp( potential2 ) 
                        ratio2 = ratio2 / ratio2.mean()
                        D_mmd = mmd2(x, y, x2, y2, ratio, ratio2, beta=mmd_beta) 

                    else: 
                        D_mmd = mmd(x, y, ratio, beta=mmd_beta)
                else: 
                    # ratio is outside
                    if mmd_two_sample: 
                        potential = G(x)  
                        potential2 = G(x2) 
                        ratio = torch.exp( potential ) 
                        ratio2 = torch.exp( potential2 ) 
                        D_mmd = mmd2(x, y, x2, y2, ratio, ratio2, beta=mmd_beta) 
                        D_mmd /= ((ratio.mean() + ratio2.mean())/2)**2

                    else:
                        # most likely this will be the same
                        potential = G(x)  
                        ratio = torch.exp( potential ) 
                        D_mmd = mmd(x, y, ratio, beta=mmd_beta) 
                        D_mmd /= (ratio.mean())**2

            else:
                # Σ delta_xi, Σ exp(G(xi)-G(yi))/ Z delta_yi
                potential = G(x) - G(y)
                ratio = torch.exp( potential ) 
                ratio = ratio / ratio.mean()
                D_diff = D(x) - D(y) * ratio
                loss = D_diff.mean()  

                if mmd_ratio_in: 
                    if mmd_two_sample: 
                        potential2 = G(x2) - G(y2)
                        ratio2 = torch.exp( potential2 ) 
                        ratio2 = ratio2 / ratio2.mean()
                        D_mmd = mmd2(x, y, x2, y2, torch.ones_like(ratio), ratio, ratio2, beta=mmd_beta)
                    else: 
                        D_mmd = mmd_r2(x, y, torch.ones_like(ratio) , ratio, beta=mmd_beta)

                else: 
                    raise NotImplementedError("hard to move outside: because the importance ratio is not matched in scale: one is one, the other is ratio")

            disc_zero = _.get_value('disc_zero')

            # lipschitz for Discriminator 
            D_grad = keep_grad(  D(x).sum(), x)

            # two way for the l2 penalty 
            # zero or one 
            if disc_zero: 
                l2_penalty = (D_grad * D_grad).sum(1).mean() * l2  # penalty to enforce f \in F
            else: 
                l2_penalty = ( torch.norm(D_grad, dim=1) -1  ).square().mean() * l2  # penalty to enforce f \in F


            # adversarial training!
            if d_iters > 0 and itr % (g_iters + d_iters) < d_iters : 
                (-1.0 * loss + l2_penalty).backward()
                D_optimizer.step()

                if clip_D: 
                    # Clip weights of discriminator
                    for p in D.parameters():
                        p.data.clamp_(-clip_value, clip_value)
                    
            else:
                if G_loss == 'GAN': 
                    loss.backward()
                elif G_loss == 'MMD': 
                    D_mmd.backward()
                elif G_loss == 'GAN + MMD': 
                    (loss + D_mmd).backward()
                else: 
                    raise NotImplementedError("The loss for the generator of type {} is not implemented".format(G_loss))


                G_optimizer.step()

            new_dict = { 
                'Discriminator': tc( -1.0 * loss + l2_penalty ), 
                'Generator': tc( loss ), 
                'MMD': tc(D_mmd), 
                'l2 penalty': tc(l2_penalty)
            }

            wandb.log(new_dict)

            if itr % viz_freq == 0:
                # figure out the domain for plots 

                if model == 'dw': 
                    # TODO: change this to the init data 
                    x = np.arange(-4.0, 4.0, 0.1)
                    y = np.arange(-4.0, 4.0, 0.1)

                    _X, _Y = np.meshgrid(x, y)
                    z0 = np.concatenate([_X.reshape(-1, 1), _Y.reshape(-1, 1)], axis=1)
                    # assert dim == 2
                    # need to consider how these goes to high dimension 
                    z0 = torch.tensor(z0, requires_grad=True).float().to(device)

                    potential = G(z0)
                    potential = tc(potential)
                    exp_pot = np.exp( potential )
                    prob = exp_pot / exp_pot.mean()
                    #  Q: do we need to multiple some constant? space volume? 

                    Z = prob.reshape(len(_X), len(_X[0]))

                    critic = D(z0)
                    critic = tc(critic)
                    critic = critic.reshape(len(_X), len(_X[0]))
                    X_list.append(_X)
                    Y_list.append(_Y)
                    Z_list.append(Z)
                    D_list.append(critic)
                    
                elif model == 'mb': 
                    x = np.arange(-2, 1, 0.04)
                    y = np.arange(-0.5, 2.5, 0.04)

                    fname = "{}_d{}.pkl".format(model, dim)
                    fname = os.path.join("./dataset/init", fname)
                    x_data = load(fname)
                    z0 = x_data["x"][:2000]

                    xi = x_data['x'][:2000, 0]
                    yi = x_data['x'][:2000, 1]
                    
                    z0 = torch.tensor(z0, requires_grad=True).float().to(device)

                    potential =  G(z0) 
                    potential = tc(potential)
                    exp_pot = np.exp( potential )
                    prob = exp_pot / exp_pot.mean() 
                    zi = griddata((xi, yi), prob, (x[None,:], y[:,None]), method='cubic')

                    critic = D(z0)
                    critic = tc(critic)
                    di = griddata((xi, yi), critic, (x[None,:], y[:,None]), method='cubic')

                    X_list.append(x)
                    Y_list.append(y)
                    Z_list.append(zi)
                    D_list.append(di)
                    
            log_freq = _.get_value('log_freq')
            if itr % log_freq == 0: 
                # log the nn checkpoint 
                model_path = os.path.join(exp_dir, 'model')
                make_dir(model_path)
                torch.save(G.state_dict(), os.path.join(model_path, 'G.pt'))
                torch.save(D.state_dict(), os.path.join(model_path, 'D.pt'))
                
                # log the animation
                new_dict = { 
                    'X': X_list, 
                    'Y': Y_list, 
                    'Z': Z_list, 
                    'D': D_list

                }

                # vis directary
                vis_dir = os.path.join(exp_dir, "vis")
                make_dir(vis_dir)
                fname = "{}_d{}.pkl".format(model, dim)
                dump(new_dict, os.path.join(vis_dir, fname))

        new_dict = { 
            'X': X_list, 
            'Y': Y_list, 
            'Z': Z_list, 
            'D': D_list
        }

        # vis directary
        vis_dir = os.path.join(exp_dir, "vis")
        make_dir(vis_dir)
        fname = "{}_d{}.pkl".format(model, dim)
        dump(new_dict, os.path.join(vis_dir, fname))


