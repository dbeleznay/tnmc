package tnmc::security::session;

use strict;
use CGI;
use tnmc::db;

#
# module configuration
#

use Exporter;
use vars qw(@ISA @EXPORT @EXPORT_OK
            );

@ISA = qw(Exporter);

@EXPORT = qw();

@EXPORT_OK = qw();

#
# module vars
#

#
# module routines
#

sub get_session{
    my ($sessionID, $session) = @_;
    
    # make sure we have a handle
    my $dbh = tnmc::db::db_connect();
    
    # fetch from the db
    my $sql = "SELECT * from SessionInfo WHERE sessionID = ?";
    my $sth = $dbh->prepare($sql) or die "Can't prepare $sql:$dbh->errstr\n";
    $sth->execute($sessionID);
    $session = $sth->fetchrow_hashref();
    $sth->finish;
}

sub set_session{
    my ($session) = @_;
    
    # make sure we have a handle
    my $dbh = tnmc::db::db_connect();
    
    my @key_list = sort( keys(%$session) );
    my $key_list = join ( ',', @key_list);
    my $ref_list = join ( ',', (map {sprintf '?'} @key_list) );
    my @var_list = map {$session->{$_}} @key_list;
    
    # save to the db
    my $sql = "REPLACE INTO SessionInfo ($key_list) VALUES($ref_list)";
    my $sth = $dbh->prepare($sql) or die "Can't prepare $sql:$dbh->errstr\n";
    $sth->execute(@var_list) or return 0;
    
    $sth->finish;
}

sub del_session{
    my ($sessionID) = @_;
    
    # make sure we have a handle
    my $dbh = tnmc::db::db_connect();
    
    # fetch from the db
    my $sql = "DELETE from SessionInfo WHERE sessionID = ?";
    my $sth = $dbh->prepare($sql) or die "Can't prepare $sql:$dbh->errstr\n";
    $sth->execute($sessionID);
    $sth->finish;
}

sub revoke_session{
    my ($sessionID) = @_;
    
    # make sure we have a handle
    my $dbh = tnmc::db::db_connect();
    
    # save to the db
    my $sql = "UPDATE SessionInfo SET open = 0 WHERE sessionID = ?";
    my $sth = $dbh->prepare($sql) or die "Can't prepare $sql:$dbh->errstr\n";
    $sth->execute($sessionID) or return 0;
    
    $sth->finish;
}

sub hit_session{
    my ($sessionID) = @_;
    
    # make sure we have a handle
    my $dbh = tnmc::db::db_connect();
    
    # save to the db
    my $sql = "UPDATE SessionInfo SET hits = (hits + 1), lastOnline = NULL WHERE sessionID = ?";
    my $sth = $dbh->prepare($sql) or die "Can't prepare $sql:$dbh->errstr\n";
    $sth->execute($sessionID) or return 0;
    
    $sth->finish;
}

1;