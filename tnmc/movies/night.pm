package tnmc::movies::night;

use strict;

#
# module configuration
#
BEGIN {
    
    use tnmc::db;
    
    use Exporter;
    use vars qw(@ISA @EXPORT @EXPORT_OK);
    
    @ISA = qw(Exporter);
    @EXPORT = qw(set_night get_night get_next_night list_nights list_future_nights list_active_nights);
    @EXPORT_OK = qw();
    
}

#
# module routines
#

sub set_night{
    my (%night, $junk) = @_;
    my ($sql, $sth, $return);
    
    &db_set_row(\%night, $dbh_tnmc, 'MovieNights', 'nightID');
    
    if (!$night{nightID}){
        $sql = "SELECT nightID FROM MovieNights WHERE date = " . $dbh_tnmc->quote($night{date});
        $sth = $dbh_tnmc->prepare($sql) or die "Can't prepare $sql:$dbh_tnmc->errstr\n";
        $sth->execute;
        ($return) = $sth->fetchrow_array();
        $sth->finish;
    }else{
        $return = $night{nightID};
    }
    return $return;
}

sub get_night{
    my ($nightID, $night_ref, $junk) = @_;
    my ($condition);

    $condition = "(nightID = '$nightID' OR date = '$nightID')";
    &db_get_row($night_ref, $dbh_tnmc, 'MovieNights', $condition);
}

# BLOCK: get_next night
{
    my $get_next_night_cache;
sub get_next_night{
    
    ## cache it if we can
    if (defined $get_next_night_cache){
        return $get_next_night_cache;
    }
    
    my ($sql, $sth);
    
    ### BUG ALERT (?)
    
    $sql = "SELECT DATE_FORMAT(date, '%Y%m%d') FROM MovieNights WHERE date >= NOW() ORDER BY date LIMIT 1";
    $sth = $dbh_tnmc->prepare($sql) or die "Can't prepare $sql:$dbh_tnmc->errstr\n";
    $sth->execute;
    ($get_next_night_cache) = $sth->fetchrow_array();
    $sth->finish();
    
    return $get_next_night_cache;
}
}

sub list_nights{
    my ($night_list_ref, $where_clause, $by_clause, $junk) = @_;
    my (@row, $sql, $sth);

    @$night_list_ref = ();

    $sql = "SELECT nightID from MovieNights $where_clause $by_clause";
    $sth = $dbh_tnmc->prepare($sql) or die "Can't prepare $sql:$dbh_tnmc->errstr\n";
    $sth->execute;
    while (@row = $sth->fetchrow_array()){
        push (@$night_list_ref, $row[0]);
    }
    $sth->finish;

    return scalar @$night_list_ref;
}

sub list_future_nights{
    my (@row, $sql, $sth);
    
    my @night_list = ();
    
    $sql = "SELECT nightID from MovieNights WHERE date >= NOW() ORDER BY date, nightID";
    $sth = $dbh_tnmc->prepare($sql) or die "Can't prepare $sql:$dbh_tnmc->errstr\n";
    $sth->execute;
    while (@row = $sth->fetchrow_array()){
        push (@night_list, $row[0]);
    }
    $sth->finish;

    return @night_list;
}

sub list_active_nights{
    my (@row, $sql, $sth);
    
    my @night_list = ();
    
    $sql = "SELECT nightID from MovieNights WHERE date >= NOW() && movieID ORDER BY date, nightID";
    $sth = $dbh_tnmc->prepare($sql) or die "Can't prepare $sql:$dbh_tnmc->errstr\n";
    $sth->execute;
    while (@row = $sth->fetchrow_array()){
        push (@night_list, $row[0]);
    }
    $sth->finish;

    return @night_list;
}

sub list_moviegod_nights{
    my ($userID) = @_;
    
    return if (! int($userID));
    
    my (@row, $sql, $sth);
    
    my @night_list = ();
    
    $sql = "SELECT nightID from MovieNights
             WHERE date >= NOW() and godID = ?
             ORDER BY date, nightID";
    $sth = $dbh_tnmc->prepare($sql) or die "Can't prepare $sql:$dbh_tnmc->errstr\n";
    $sth->execute($userID);
    while (@row = $sth->fetchrow_array()){
        push (@night_list, $row[0]);
    }
    $sth->finish;

    return @night_list;
}

sub show_moviegod_links{
    my ($userID) = @_;
    
    use tnmc::user;
    use tnmc::util::date;
    
    # have to be logged in to touch
    return if (!$userID);

    # demo has no access
    return if ($userID == 38);
    
    my %user;
    &get_user($userID, \%user);
    
    # have to be in group movies to touch
    return if (! $user{groupMovies});
    
    # get moviegod nights
    my @nights = &list_moviegod_nights($userID);
    
    if (scalar @nights){
        print "Be a Movie God:\n";
        foreach my $nightID (@nights){
            my %night;
            &get_night($nightID, \%night);
            print "<a href=\"\/movies\/night_edit.cgi?nightID=$nightID\">", &tnmc::util::date::format_date('short_date', $night{date}), "</a>\n";
            print " - " if ($nightID ne $nights[scalar(@nights) - 1]);
        }
    }
}


1;
