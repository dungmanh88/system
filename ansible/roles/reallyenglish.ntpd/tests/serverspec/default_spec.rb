require 'spec_helper'

package = 'ntp'
service = 'ntp'
config  = '/etc/ntp.conf'
db_dir  = '/var/lib/ntp'

case os[:family]
when 'freebsd'
  db_dir = '/var/db/ntp'
  service = 'ntpd'
when 'redhat'
  service = 'ntpd'
end
puts os[:family]

leap_file = "#{ db_dir }/leap-seconds.list"

case os[:family]
when 'freebsd'
else
  describe package(package) do
    it { should be_installed }
  end 
end

case os[:family]
when 'redhat'
  describe package('libselinux-python') do
    it { should be_installed }
  end
end

describe file(config) do
  it { should be_file }
  its(:content) { should match Regexp.escape('server 0.pool.ntp.org') }
  its(:content) { should match Regexp.escape('server 1.pool.ntp.org') }
  its(:content) { should match Regexp.escape('server 2.pool.ntp.org') }
  its(:content) { should match Regexp.escape('server 3.pool.ntp.org') }
end

describe file(leap_file) do
  it { should be_file }
  its(:content) { should match(/2272060800\s+10\s+/) }
end

describe service(service) do
  it { should be_running }
  it { should be_enabled }
end
