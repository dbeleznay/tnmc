package tnmc::util::temp;

use strict;
use tnmc::util::file;

BEGIN{
    use vars qw($temp_path);
    $temp_path = "/tmp/"
}

#
# module routines
#

sub get_dir{
    
    my $PID = $$;
    
    # get a unique name
    my $dir = $lang::config::temp_dir . 'tnmc_' . $PID . '/';
    my $i;
    while (-e $dir) {
        $i++;
        $dir = $lang::config::temp_dir . 'tnmc_' . $PID . '_' . $i . '/';
    }
    
    # make the dir
    &lang::util::file::make_directory($dir);
    
    # return the dir name
    return $dir;
}

sub kill_dir{
    my ($dir) = @_;
    
    # make sure it's actually in the data/temp dir.
    return 0 if ($dir !~ /^$lang::config::temp_dir\/tnmc/);
    
    # delete the dir
    &lang::util::file::kill_tree($dir);
    
    return 1;
}

1;

