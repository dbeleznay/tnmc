#!/usr/bin/perl

##################################################################
#       Scott Thompson - scottt@interchange.ubc.ca
##################################################################
### Opening Stuff. Modules and all that. nothin' much interesting.

### minor modifications by Grant 00-11-24 to add in quick buttons for sorting table

use strict;
use lib '/tnmc';

use tnmc::security::auth;
use tnmc::db;
use tnmc::user;
use tnmc::cgi;
use tnmc::template;
use tnmc::movies::attend;
use tnmc::movies::movie;
use tnmc::movies::show;
use tnmc::movies::vote;
use tnmc::movies::attendance;
use tnmc::movies::night;

#############
### Main logic

&db_connect();
&header();
my $tnmc_cgi = &tnmc::cgi::get_cgih();


## Variables
my $sortOrder = $tnmc_cgi->param('sortOrder') || 'order';

my $e_userID = $USERID;

if (($USERID{groupMovies} >= 100) && ($tnmc_cgi->param('effectiveUserID')) ){
    $e_userID = $tnmc_cgi->param('effectiveUserID');
}

my @nights = &list_future_nights();
my $nightID = $nights[0];

&show_local_nav($sortOrder, $e_userID, $USERID, $nightID);
&show_my_attendance_chooser($e_userID);
&show_movies_enhanced($sortOrder, $e_userID, $USERID, $nightID);

&footer();
&db_disconnect();


##########################################################
sub show_local_nav{
    my ($sortOrder, $effectiveUserID, $real_userID, $nightID) = @_;
    
    my %REAL_USER;
    &get_user($real_userID, \%REAL_USER);
    
    my %sortSel;
    $sortSel{$sortOrder} = 'selected';
    
    print qq{
        <form action="index.cgi" method="get">
        <table border="0" cellpading="0" cellspacing="0" ><tr valign="top">
          <td>
              <font face="verdana" size="-1" color="888888"><b>
              sort by</b><br>
              <select name="sortOrder" onChange="form.submit();">
                  <option $sortSel{title} value="title">Title
                  <option $sortSel{rank} value="rank">Rank (\#)
                  <option $sortSel{order} value="order">Order
                  <option $sortSel{votesFor} value="votesForTotal">Votes For (+)
                  <option $sortSel{votesAgainst} value="votesAgainst">Votes Against (-)
                  <option $sortSel{votesAway} value="votesAway">Votes Away (grey)
                  <option $sortSel{movieID} value="movieID">Movie ID
                  <option  value="$sortOrder">
                  <option $sortSel{rating} value="rating">Rating
                  <option $sortSel{type} value="type">Type
                  <option $sortSel{theatres} value="theatres">Theatres
              </select>
          </td>
    };
    
    ## let admin users modify other people's votes
    if ($REAL_USER{groupMovies} >= 100){
        print qq{
                <td>
                    <font face="verdana" size="-1" color="888888"><b>modify votes for</b><br>
                    <select name="effectiveUserID" onChange="form.submit();">
        };
        
        my $sql = "SELECT userID, username FROM Personal WHERE groupMovies >= 1  ORDER BY username";
        my $sth = $dbh_tnmc->prepare($sql);
        $sth->execute();
        
        while (my ($userID, $username) = $sth->fetchrow_array()){
            my $sel = ($userID == $effectiveUserID)? 'selected' : '';
            print qq{           <option value="$userID" $sel>$username \n };
        }
        $sth->finish();
        print qq{    </select>     </td>      };
    }
    
    print qq{    </tr></table></form>   };
    
    
}

##########################################################
sub show_movies_enhanced{
    my ($sortOrder, $effectiveUserID, $real_userID, $nightID) = @_;
    
    my %REAL_USER;
    &get_user($real_userID, \%REAL_USER);
    
    my %USER;
    &get_user($effectiveUserID, \%USER);
    
    
    # mini-hack
    my $displaySortOrder = $sortOrder;
    if ( ($displaySortOrder eq 'title')
       ||($displaySortOrder eq 'rank')
       ||($displaySortOrder eq 'votesForTotal')
       ||($displaySortOrder eq 'votesAgainst')
       ||($displaySortOrder eq 'votesAway')
       ){
        $displaySortOrder = ''
    }
    
    my %night;
    &get_night($nightID, \%night);
    
    &show_heading ("Detailed Votes - $night{'date'}");
    
    ##################################################################
    ### Start of list
    ### modifications by Grant 00-11-24 to add in quick buttons for sorting
    print qq{
        <table cellpadding="0" cellspacing="0" border="0">
            <tr  bgcolor="ffffff">
                <td><b>Edit</b></td>
            <td align="center"><b>&nbsp;N&nbsp;&nbsp;?&nbsp;&nbsp;Y&nbsp;</b></td>
            <td align="right">&nbsp;&nbsp;<a href="index.cgi?sortOrder=rank&effectiveUserID=$effectiveUserID"><b>#</b></a></td>
            <td align="right">&nbsp;&nbsp;<a href="index.cgi?sortOrder=votesFor&effectiveUserID=$effectiveUserID"><b>+</b></a></td>
            <td align="right">&nbsp;&nbsp;<a href="index.cgi?sortOrder=votesAgainst&effectiveUserID=$effectiveUserID"><b>-</b></a></td>
            <td>&nbsp;&nbsp;</td>
            <td><a href="index.cgi?sortOrder=title&effectiveUserID=$effectiveUserID"><b>Title</b></a></td>
            <td>&nbsp;&nbsp;</td>
            <td><b>$displaySortOrder</b></td>
            <td>&nbsp;&nbsp;</td>
            <td><b>Votes</b></td>
            </tr>
        <tr>
            <td colspan="11" bgcolor="cccccc" align="right">
                <form action="/movies/update_votes.cgi" method="post">
                <input type="hidden" name="userID" value="$effectiveUserID">
                <font color="888888"><b>now showing </td></tr>
    };
    
    ########################
    # Now Showing
    show_movie_list_enhanced( "WHERE (statusShowing AND ( NOT (statusSeen OR 0)) AND NOT (statusBanned or 0) )", 
                              $displaySortOrder, $effectiveUserID, $sortOrder, $nightID);
    
    print qq{    <tr>
            <td colspan="11" bgcolor="cccccc" align="right">
            <font color="888888"><b>coming soon </td></tr>
    };
    
    ########################
    # Coming Soon
    show_movie_list_enhanced( "WHERE (statusNew AND NOT (statusShowing OR 0))", 
                              $displaySortOrder, $effectiveUserID, $sortOrder, 0);
    
    print qq{\n    </table><p>\n};
    
    ### End of list
    ##################################################################


    ########################
    ### Do the Favorite Movie Stuff
    
    print qq{
        <font face="verdana">
        <b>Favorite Movie:</b><br>
    };
    &show_favorite_movie_select($effectiveUserID);
    print qq{
        <br></font>
    };


    ########################
    ### Do the Favorite Movie Stuff
    if ($REAL_USER{groupMovies} >= 100){
        print qq{
            <font face="verdana">
            <b>Super Favorite Movie:</b><br>
        };
        &show_superfavorite_movie_select($effectiveUserID);
        print qq{
            <br></font>
        };
    }
    ########################
    ### Warn if modifying another user's votes.
    
    my $useridNotice = '';
    if ($effectiveUserID != $USERID){
        $useridNotice = qq{
            <font face="arial" size="+1" color="086DA5"><i><b>
                for $USER{username}</b></i></font>
        };
    }

    ########################
    ### Show the Update Votes buton.
    
    print qq{
        <input type="image" border="0" src="/template/update_votes_submit.gif"
                 alt="Update Votes">$useridNotice
        </form>
    };
}


##########################################################
sub show_movie_list_enhanced {
    
    my ($whereClause, $extraField, $effectiveUserID, $sortOrder, $nightID) = @_;
    
    my (@movies, $anon, $movieID, %movieInfo);
    my ($boldNew, %vote_status_word, @list);
    
    &list_movies(\@list, $whereClause, 'ORDER BY title');
    foreach my $movieID (@list){
        my $anon = {};     ### create an anonymous hash.
        &get_movie_extended2($movieID, $anon, $nightID);
        $movieInfo{$movieID} = $anon;
    }
    if ($sortOrder){
        ## Note: if we say 'rank', we really mean 'order' (more granularity)
        $sortOrder = 'order' if ($sortOrder eq 'rank');

        @list = sort  {
            (   ($movieInfo{$b}->{$sortOrder}
                 <=>     $movieInfo{$a}->{$sortOrder})
                ||
                ($movieInfo{$a}->{$sortOrder}
                 cmp     $movieInfo{$b}->{$sortOrder})
                )
            }
            @list ;
    }
    
    foreach my $movieID (@list){
        
        my $vote = &get_vote($movieID, $effectiveUserID);
        
        my %vote_status_word;
        $vote_status_word{$vote} = "CHECKED";
        
        print qq{
            <tr valign="top">
                <td><a href="movie_edit.cgi?movieID=$movieID"><font color="cccccc">$movieID</a></td>
                <td valign="top" nowrap><input type="radio" name="v$movieID" value="-1" $vote_status_word{'-1'}><input type="radio" name="v$movieID" value="0" $vote_status_word{'0'}><input type="radio" name="v$movieID" value="1" $vote_status_word{'1'} $vote_status_word{'2'}></td>
                <td align="right">$movieInfo{$movieID}->{rank}</td>
                <td align="right">$movieInfo{$movieID}->{votesForTotal}</td>
                <td align="right">$movieInfo{$movieID}->{votesAgainst}</td>
                <td></td>
                <td valign="top">
        };
        if ( ($movieInfo{$movieID}->{statusShowing}) &&($movieInfo{$movieID}->{statusNew}) ){ print qq{<b>}; }
        print qq{
                    <a href="movie_view.cgi?movieID=$movieID" target="viewmovie">
                        $movieInfo{$movieID}->{title}</a></td>
                <td></td>
                <td>$movieInfo{$movieID}->{$extraField}</td>
                <td></td>
                <td>$movieInfo{$movieID}->{votesHTML}</td>

            </tr>
        };

    }
}


##########################################################
#### The end.
##########################################################
