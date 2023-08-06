import pyro
import pyro.distributions as dist
import torch

from pyro import poutine
from pyro.infer.autoguide import AutoDelta
import numpy as np
from congas.models.Model import Model
from congas.utils import log_sum_exp
import congas.building_blocks as lks

from sklearn.cluster import KMeans
import torch.distributions as tdist



class LatentCategorical(Model):
    params = {'K': 2, 'probs': torch.tensor([0.2, 0.3, 0.3, 0.1, 0.1]), 'hidden_dim': 5, 'a' : 1, 'b' : 100,
              'theta_shape_rna': None, 'theta_rate_rna': None,'theta_shape_atac': None, 'theta_rate_atac': None,
              'batch_size': None, "init_probs" : 5, 'norm_init_sd_rna' : None, "norm_init_sd_atac" : None,
              'mixture': None, "nb_size_init_atac": None,"nb_size_init_rna": None, "binom_prior_limits" : [10,10000],
              "likelihood_rna" : "NB", "likelihood_atac" : "NB", 'lambda' : 1, "latent_type" : "D", "Temperature" : 1/100}

    data_name = set(['data_rna', 'data_atac', 'pld', 'segments', 'norm_factor_rna', 'norm_factor_atac'])

    def __init__(self, data_dict):
        self._params = self.params.copy()
        self._data = None
        super().__init__(data_dict, self.data_name)

    def model(self,i = 1,  *args, **kwargs):

        Temperature = self._params['Temperature'] / i

        ### CHeck the existence of the single modality and get its dimensions
        if 'data_rna' in self._data:
            I, N = self._data['data_rna'].shape
            batch1 = N if self._params['batch_size'] else self._params['batch_size']
            #rho_r
            weights_rna = pyro.sample('mixture_weights_rna',
                                  dist.Dirichlet((1. / self._params['K']) * torch.ones(self._params['K'])))

        if 'data_atac' in self._data:
            I, M = self._data['data_atac'].shape
            batch2 = M if self._params['batch_size'] else self._params['batch_size']
            # rho_a
            weights_atac = pyro.sample('mixture_weights_atac',
                                  dist.Dirichlet((1. / self._params['K']) * torch.ones(self._params['K'])))

        cat_vector = torch.tensor(np.arange(self._params['hidden_dim']) + 1, dtype=torch.float)


        with pyro.plate('segments', I):

            ### RNA segment dependent factors ###
            if 'data_rna' in self._data:
                if self._params["likelihood_rna"] == "NB":
                    #size_r
                    sizes_rna = pyro.sample("NB_size_rna", dist.Uniform(self._params['binom_prior_limits'][0],
                                                                self._params['binom_prior_limits'][1]))



                if self._params["likelihood_rna"] in ["N", "G"]:
                    # sd_r
                    norm_sd_rna = pyro.sample('norm_sd_rna', dist.Uniform(self._params['a'], self._params['b']))
                    segment_factor_rna = torch.ones(I)
                else :
                    # theta_e
                    segment_factor_rna = pyro.sample('segment_factor_rna',
                                                     dist.Gamma(self._params['theta_shape_rna'],
                                                                self._params['theta_rate_rna']))

            ### ATAC segment dependent factors ###
            if 'data_atac' in self._data:
                # size_a
                if self._params["likelihood_atac"] == "NB":
                    sizes_atac = pyro.sample("NB_size_atac", dist.Uniform(self._params['binom_prior_limits'][0],
                                                                self._params['binom_prior_limits'][1]))


                if self._params["likelihood_atac"] in ["N", "G"]:
                    # sd_a
                    norm_sd_atac = pyro.sample('norm_sd_atac', dist.Uniform(self._params['a'], self._params['b']))
                    segment_factor_atac = torch.ones(I)

                else:
                    # theta_a
                    segment_factor_atac = pyro.sample('segment_factor_atac',
                                                      dist.Gamma(self._params['theta_shape_atac'],
                                                                 self._params['theta_rate_atac']))

            ### MODALITY INDEPENDENT HIDDEN CNV VALUES ###
            with pyro.plate('components', self._params['K']):
                # C
                cc = pyro.sample("CNV_probabilities", dist.Dirichlet(self._params['probs']))

        ### MEAN FILED-LIKE MODEL ###
        # E[lk(x_ni | z_nk)] = segment_factor_i * CNA_k * norm_factor_n
        # CNA_k = rho_k * [1,...,5]


        lk_rna = 0
        if 'data_rna' in self._data:

            with pyro.plate('data_rna', N, batch1):
                # p(x|z_i) = Poisson(marg(cc * theta * segment_factor))

                if self._params["latent_type"] == "D":

                    if self._params["likelihood_rna"] == "NB":
                        lk_rna = lks.NB_likelihood2(self, segment_factor_rna, cc, cat_vector, weights_rna, sizes_rna, "rna")

                    elif self._params["likelihood_rna"] == "P":
                        lk_rna = lks.poisson_likelihood2(self,segment_factor_rna,cc,cat_vector, weights_rna, "rna")

                    else:
                        lk_rna = lks.gaussian_likelihood2(self, segment_factor_rna,cc,cat_vector, weights_rna, norm_sd_rna, "rna")

                else:
                    segment_fact_cat = torch.matmul(segment_factor_rna.reshape([I, 1]),
                                                    cat_vector.reshape([1, self._params['hidden_dim']]))

                    gumble = tdist.Gumbel(0, 1).sample(cc.shape)
                    cc_argmax = ((torch.log(cc) + gumble)/Temperature).softmax(-1)


                    segment_fact_marg_rna = segment_fact_cat * cc_argmax

                    print(segment_fact_marg_rna[:, 5, :])

                    segment_fact_marg_rna = torch.sum(segment_fact_marg_rna, dim=-1)

                    if self._params["likelihood_rna"] == "NB":
                        lk_rna = lks.NB_likelihood(self, segment_fact_marg_rna, weights_rna, sizes_rna, "rna")

                    elif self._params["likelihood_rna"] == "P":
                        lk_rna = lks.poisson_likelihood(self, segment_fact_marg_rna, weights_rna, "rna")

                    else:
                        lk_rna = lks.gaussian_likelihood(self, segment_fact_marg_rna, weights_rna, norm_sd_rna, "rna")

        lk_atac = 0

        if 'data_atac' in self._data:

            with pyro.plate('data_atac', M, batch2):
                # p(x|z_i) = Poisson(marg(cc * theta * segment_factor))


                if self._params["latent_type"] == "D":

                    if self._params["likelihood_atac"] == "NB":
                        lk_atac = lks.NB_likelihood2(self, segment_factor_atac,cc, cat_vector, weights_atac, sizes_atac, "atac")
                    elif self._params["likelihood_atac"] == "P":
                        lk_atac = lks.poisson_likelihood2(self, segment_factor_atac,cc, cat_vector, weights_atac, "atac")
                    else:
                        lk_atac = lks.gaussian_likelihood2(self, segment_factor_atac,cc,cat_vector, weights_atac, norm_sd_atac, "atac")

                else:

                    segment_fact_cat_atac = torch.matmul(segment_factor_atac.reshape([I, 1]),
                                                    cat_vector.reshape([1, self._params['hidden_dim']]))

                    gumble = tdist.Gumbel(0, 1).sample(cc.shape)
                    cc_argmax = ((torch.log(cc) + gumble) / Temperature).softmax(-1)
                    segment_fact_marg_atac = segment_fact_cat_atac * cc_argmax
                    segment_fact_marg_atac = torch.sum(segment_fact_marg_atac, dim=-1)


                    if self._params["likelihood_atac"] == "NB":
                        lk_atac = lks.NB_likelihood(self, segment_fact_marg_atac, weights_atac, sizes_atac, "atac")
                    elif self._params["likelihood_atac"] == "P":
                        lk_atac = lks.poisson_likelihood(self, segment_fact_marg_atac, weights_atac, "atac")
                    else:
                        lk_atac = lks.gaussian_likelihood(self, segment_fact_marg_atac, weights_atac, norm_sd_atac, "atac")

        pyro.factor("lk", self._params['lambda'] * lk_rna + (1-self._params['lambda']) * lk_atac)



    def guide(self,expose, *args, **kwargs):
        return AutoDelta(poutine.block(self.model, expose=expose),
                         init_loc_fn=self.init_fn())

    def init_fn(self):

        def init_function(site):
            if site["name"] == "CNV_probabilities":
                return self.create_dirichlet_init_values()
            if site["name"] == "mixture_weights_rna":
                return self._params['mixture']
            if site["name"] == "mixture_weights_atac":
                return self._params['mixture']
            if site["name"] == "NB_size_rna":
                return self._params['nb_size_init_rna']
            if site["name"] == "NB_size_atac":
                return self._params['nb_size_init_atac']
            if site["name"] == "norm_sd_rna":
                return self._params['norm_init_sd_rna']
            if site["name"] == "norm_sd_atac":
                return self._params['norm_init_sd_atac']
            if site["name"] == "segment_factor_rna":
                return dist.Gamma(self._params['theta_shape_rna'], self._params['theta_rate_rna']).mean
            if site["name"] == "segment_factor_atac":
                return dist.Gamma(self._params['theta_shape_atac'], self._params['theta_rate_atac']).mean
            raise ValueError(site["name"])

        return init_function

    def create_dirichlet_init_values(self):

        if 'data_atac' in self._data:
            I, N = self._data['data_atac'].shape
            data = self._data['data_atac']
            nf = self._data['norm_factor_atac']
            sf = dist.Gamma(self._params['theta_shape_atac'], self._params['theta_rate_atac']).mean.reshape([I, 1])


        else:
            I, N = self._data['data_rna'].shape
            data = self._data['data_rna']
            nf = self._data['norm_factor_rna']
            sf = dist.Gamma(self._params['theta_shape_rna'], self._params['theta_rate_rna']).mean.reshape([I,1])


        init_prob_high = self._params['init_probs']
        low_prob = (1 - init_prob_high) / (self._params['hidden_dim'] - 1)
        high_prob = init_prob_high

        X = (data / sf)
        X = X / nf
        X = X.detach().numpy()

        kmat = torch.zeros(self._params['K'], I)

        for i in range(len(self._data['pld'])):
            km = KMeans(n_clusters=self._params['K'], random_state=0).fit(X[i,].reshape(-1, 1))
            centers = torch.tensor(km.cluster_centers_).flatten()
            for k in range(self._params['K']):
                kmat[k, i] = centers[k]

        init = torch.zeros(self._params['K'], I, self._params['hidden_dim'])

        for i in range(len(self._data['pld'])):
            for j in range(self._params['hidden_dim']):
                for k in range(self._params['K']):
                    if k == 0:
                        init[k, i, j] = high_prob if (j + 1) == torch.round(kmat[k,i]) else low_prob
                    else:
                        init[k, i, j] = high_prob if (j + 1) == torch.round(kmat[k,i]) else low_prob

        return init



    def likelihood(self, inf_params, mod = "rna",sum = False):

        Temperature = self._params['Temperature'] / 1000
        I, N = self._data['data_{}'.format(mod)].shape
        cat_vector = torch.tensor(np.arange(self._params['hidden_dim']) + 1, dtype=torch.float)


        if self._params["likelihood_{}".format(mod)] in ["G", "N"]:
            segment_fact = torch.ones(I)
        else:
            segment_fact = inf_params["segment_factor_{}".format(mod)]

        segment_fact = torch.matmul(segment_fact.reshape([I, 1]),
                                    cat_vector.reshape([1, self._params['hidden_dim']]))

        gumble = tdist.Gumbel(0, 1).sample(inf_params["CNV_probabilities"].shape)

        cc_argmax = ((torch.log(inf_params["CNV_probabilities"]) + gumble) / Temperature).softmax(-1)





        segment_fact_marg = segment_fact * cc_argmax



        segment_fact_marg = torch.sum(segment_fact_marg, dim=-1)

        print(segment_fact_marg[:, :])


        if self._params["likelihood_{}".format(mod)] == "NB":
            if self._params["latent_type"] == "D":
                lk = lks.NB_likelihood_aux(self, segment_fact_marg, inf_params["NB_size_{}".format(mod)], mod)
            else:
                lk = lks.NB_likelihood_aux2(self, inf_params["segment_factor_{}".format(mod)],
                                           inf_params["CNV_probabilities"],
                                           cat_vector,
                                           inf_params["NB_size_{}".format(mod)], mod)

        elif self._params["likelihood_{}".format(mod)] == "P":
            if self._params["latent_type"] == "D":
                lk = lks.poisson_likelihood_aux2(self, inf_params["segment_factor_{}".format(mod)],
                                            inf_params["CNV_probabilities"],
                                            cat_vector, mod)
            else:
                lk = lks.poisson_likelihood_aux(self, segment_fact_marg, mod)

        else:
            if self._params["latent_type"] == "D":
                lk = lks.gaussian_likelihood_aux2(self, inf_params["segment_factor_{}".format(mod)],
                                                 inf_params["CNV_probabilities"],
                                                 cat_vector,
                                                inf_params["norm_sd_{}".format(mod)],
                                                  mod)
            else:
                lk = lks.gaussian_likelihood_aux(self, segment_fact_marg, inf_params["norm_sd_{}".format(mod)], mod)

        if(sum):
            lk = lk + torch.log(inf_params["mixture_weights_{}".format(mod)]).reshape([len(inf_params["mixture_weights_{}".format(mod)]), 1, 1])
            lk = log_sum_exp(lk).sum()

        return lk


    def calculate_cluster_assignements(self, inf_params):

        res = {}
        ### CLUSTER ASSIGNMENTS FOR RNA ###

        if 'data_rna' in self._data:
            lk = self.likelihood(inf_params, "rna")
            # p(z_i| D, X ) = lk(z_i) * p(z_i | X) / sum_z_i(lk(z_i) * p(z_i | X))
            # log(p(z_i| D, X )) = log(lk(z_i)) + log(p(z_i | X)) - log_sum_exp(log(lk(z_i)) + log(p(z_i | X)))
            lk = torch.sum(lk, dim=1) + torch.log(inf_params["mixture_weights_rna"]).reshape([self._params['K'], 1])

            summed_lk = log_sum_exp(lk)
            ret_rna = lk - summed_lk
            ret_rna = torch.exp(ret_rna)
            res["assignment_probs_rna"] = ret_rna
            res["assignment_rna"] = torch.argmax(ret_rna, axis = 0)



        ### CLUSTER ASSIGNMENTS FOR DNA ###

        if 'data_atac' in self._data:
            lk = self.likelihood(inf_params, "atac")
            lk = torch.sum(lk, dim=1) + torch.log(inf_params["mixture_weights_atac"]).reshape([self._params['K'], 1])
            print(lk)
            summed_lk = log_sum_exp(lk)
            ret_atac = lk - summed_lk
            ret_atac = torch.exp(ret_atac)
            res["assignment_probs_atac"] = ret_atac
            res["assignment_atac"] = torch.argmax(ret_atac, axis = 0)

        return res