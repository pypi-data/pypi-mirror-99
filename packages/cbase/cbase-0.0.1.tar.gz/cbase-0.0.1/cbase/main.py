import os

from cbase import config, utils, repo

###########################################################################
class CB:
    def __init__(self, 
                 path="",
                 debug=False,
                 con=False,
                 print_json=False,
                 print_line_around_json=False):

        """
        Main class
        
        Args:
             path (str): path to all repositories (optional; use $USER/CB)
             debug (bool): True: raise exception instead of soft exit

        """

        # Configuration
        self.cfg = {}

        # Update with static config
        self.cfg.update(config.cfg)

        # Run-time parameters
        self.rt = {}

        # Set path to all repositories
        #   Check 1) explicit path from above
        #         2) environment variable CM_HOME
        #         3) USER HOME directory CM
        home_path = path 
        
        if home_path == '':
           home_path = os.environ.get(self.cfg['env_home'],'')

        if home_path == '':
           from os.path import expanduser
           home_path = os.path.join(expanduser("~"), self.cfg['default_home_dir'])

        self.rt['home_path'] = home_path

        # Check external config file
        config_file = os.path.join(home_path, self.cfg['config_file'])

        if os.path.isfile(config_file):
            r = utils.load_yaml(config_file)
            self.cfg.update(r['data'])

        # Check debug
        if os.environ.get(self.cfg['env_debug'], '')!='':
            debug = True
        self.rt['debug'] = debug

        # Check console
        self.rt['con'] = con

        # Check output
        self.rt['print_json'] = print_json

        # Check if line before json
        self.rt['print_line_around_json'] = print_line_around_json

        # Check file with databases
        self.rt['file_repo_list'] = os.path.join(home_path, self.cfg['file_repo_list'])

        # Load repositories or initialize empty file with local repos
        self.repos = []

        if os.path.isfile(self.rt['file_repo_list']):
            # Load info about existing repos (paths)
            r = utils.load_json(self.rt['file_repo_list'])
            self.repos = r['data']

        else:
            # Initialize local repo
            path_local_repo = os.path.join(self.rt['home_path'], self.cfg['local_repo_name'])

            ck_local_repo = repo.Repo(self)

            r = ck_local_repo.init(path = path_local_repo,
                                   desc = self.cfg['local_repo_desc'],
                                   name = self.cfg['local_repo_name'],
                                   uid = self.cfg['local_repo_uid'])
            if r['return']>0:
                self.finalize(r)


    ###########################################################################
    def finalize(self, r):
        """
        Prepare error code

        Args:
            output (dict): misc

        Returns:
            None

        """

        ret = r['return']

        if self.rt['print_json']:
            if self.rt['print_line_around_json']:
                print (self.cfg['line_before_json'])

            import json
            print (json.dumps(r, indent=2))

            if self.rt['print_line_around_json']:
                if self.cfg.get('line_after_json','') != '':
                    print (self.cfg['line_after_json'])

        if ret > 0:
            if self.rt['debug']:
                raise(Exception(r['error']))
            else:
                print (self.cfg['error_prefix']+' '+r['error'])

        exit(ret)


    
    ###########################################################################
    def access(self, i, argv=None):
        """
        Access CB repositories

        Args:
            i (dict) - CB dictionary

            (argv) (list) - original input from the command line
                            to support wrapping around tools
        """

        # Process special commands
        module = i.get('module','')

        if module == 'ck':
            # Keep support for CK
            import ck.kernel as ck

            return ck.access(argv[1:])

        data = i.get('data','')
            
        # Import fnmatch if * or ?
        module_wildcards=True if '*' in module or '?' in module else False
        data_wildcards=True if '*' in data or '?' in data else False

        if module_wildcards or data_wildcards:
            import fnmatch
        
        # Iterate over CB repos
        for p in self.repos:
            path = p['path']

            if os.path.isdir(path):
                # Expand modules
                list_of_modules=[]
                if not module_wildcards:
                    list_of_modules.append(module)
                else:
                    list_of_potential_modules = os.listdir(path)

                    for m in list_of_potential_modules:
                        if fnmatch.fnmatch(m, module):
                            list_of_modules.append(m)

                # Iterate over modules
                for m in list_of_modules:
                    pm=os.path.join(path, m)
                
                    if os.path.isdir(pm):
                        # Expand data
                        list_of_data=[]
                        if not data_wildcards:
                            list_of_data.append(data)
                        else:
                            list_of_potential_data = os.listdir(pm)

                            for d in list_of_potential_data:
                                if fnmatch.fnmatch(d, data):
                                    list_of_data.append(d)

                        # Iterate over data
                        for d in list_of_data:
                            pd=os.path.join(pm, d)

                            if os.path.isdir(pd):
                                print (pd)



        return {'return':0}
