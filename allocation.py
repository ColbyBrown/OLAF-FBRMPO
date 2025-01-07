import numpy as np
import pandas as pd
import yaml
import sys
rng = np.random.default_rng(12345)
import multiprocessing as mp
from functools import partial


## Load config details from YAML
def load_yaml(filename):
    with open(filename, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as error:
            print(error)
    return None

import time

class model:
    def __init__(self,config):
        # The initialization code should read a YAML config file and use it to define the basic parameters of the model
        self.config = load_yaml(config)
        self.option_df = pd.read_csv(self.config['location_options'])
        self.id = self.config['option_id']
        self.option_df.set_index(self.id,drop=False,inplace=True)
        self.land_uses = self.config['land_uses']
        self.draws = self.config['draws']
    def sample_alts(self,LU):
        # This method samples development options for a land use, respecting filters
        sites_avail = self.option_df.query(self.land_uses[LU]["filter_fn"]) 
        site_sample = sites_avail.sample(self.draws,replace=False,axis=0)
        return(site_sample)
    def allocate(self):
        start = time.time()
        # This method allocates land use control totals using Monte Carlo simulation
        id = self.config['option_id']
        dev_queue = [] # enumerate a "queue" of development projects to build
        for LU in self.land_uses:
            store_fld = self.land_uses[LU]["store_fld"]
            self.option_df[store_fld] = 0 # initialize field to which units will be allocated
            print("Enumerating " + self.land_uses[LU]['name'] + " to allocate")
            total = int(self.land_uses[LU]["total"])
            for draw in range(total):
                dev_queue.append(LU)
        rng.shuffle(dev_queue) # randomize the order so no specific LU gets priority
        position = 0
        progress = 0
        _last_part = 0
        print("Allocating queue...")
        for LU in dev_queue:
            position = position + 1
            progress = round(100*(position)/len(dev_queue),0)
            part = round((progress % 10)/2,0)
            if part != _last_part:
                if part == 0:
                    print(f"{progress}%")
                else:
                    print(".", end="", flush=True)
            _last_part = part
            store_fld = self.land_uses[LU]["store_fld"]
            value_fn = self.land_uses[LU]["value_fn"]
            options = self.sample_alts(LU)
            utility = options.eval(value_fn,inplace=False).to_numpy()
            expUtil = np.exp(utility)
            mask = np.isfinite(expUtil)
            expUtil = expUtil[mask]
            options = options[mask]
            if options.shape[0]==0:
                continue
            denom = np.sum(expUtil)
            probs = expUtil/denom
            zoneSel = rng.choice(options[id].to_numpy(),p=probs)
            self.option_df.at[zoneSel,store_fld] += 1
        run_min = round((time.time()-start)/60,1)
        print(f"Total run time = {run_min} minutes")
    def update(self):
        # this is a function for custom updates on the dataframe before/after allocation
        for op in self.config['update_block']:
            self.option_df.eval(op, inplace=True)

def run_allocation(config_path):
    test_model = model(config_path)
    test_model.allocate()
    test_model.update()
    return test_model.option_df

def average_results(results):
    avg_df = results[0].copy()
    for col in avg_df.columns:
        if pd.api.types.is_numeric_dtype(avg_df[col]):
            avg_df[col] = sum(df[col] for df in results) / len(results)
    return avg_df

def main():
    config_path = sys.argv[1]
    output_path = sys.argv[2]
    num_runs = 10

    with mp.Pool(processes=num_runs) as pool:
        results = pool.map(partial(run_allocation, config_path), range(num_runs))

    averaged_df = average_results(results)
    averaged_df.to_csv(output_path, index=False)

if __name__=="__main__":
    main()