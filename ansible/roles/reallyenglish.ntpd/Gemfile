source 'https://rubygems.org'

# rack 2.x requires ruby >= 2.2.2
gem 'rack', '~> 1.6.4'

gem 'rake', '~> 11.1.2'
gem 'rspec', '~> 3.4.0'
gem "test-kitchen", '~> 1.6.0'
gem "kitchen-vagrant", '~> 0.19.0'
# use patched kitchen-ansible
gem "kitchen-ansible", '~> 0.40.1', :git => 'https://github.com/trombik/kitchen-ansible.git', :branch => 'freebsd_support'
gem "kitchen-sync", '~> 2.1.1', :git => 'https://github.com/trombik/kitchen-sync.git', :branch => 'without_full_path_to_rsync'
gem 'kitchen-verifier-shell', '~> 0.2.0'
gem 'kitchen-verifier-serverspec', '~> 0.3.0'
gem 'infrataster', '~> 0.3.2', :git => 'https://github.com/trombik/infrataster.git', :branch => 'reallyenglish'
gem 'serverspec', '~> 2.37.2'
gem 'specinfra', '>= 2.63.2' # OpenBSD's `port` is fixed in this version
