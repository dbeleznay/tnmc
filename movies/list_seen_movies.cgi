#!/usr/bin/perl

##################################################################
#	Scott Thompson - scottt@interchange.ubc.ca 
##################################################################
### Opening Stuff. Modules and all that. nothin' much interesting.

use lib '/usr/local/apache/tnmc/';
use tnmc;
require 'MOVIES.pl';

	#############
	### Main logic
	
	&header();
	&db_connect();

		&show_movieMenu();
		print "<br>";

		&show_heading("Movies that we've been to");
                &show_seen_movie_list();

	&db_disconnect();
	&footer();

##########################################################
#### sub procedures.
##########################################################

#########################################
sub show_seen_movie_list{
	my (@movies, %movie, $movieID, $key);

	&list_movies(\@movies, "WHERE statusSeen = '1'", 'ORDER BY date DESC, title');
	&get_movie($movie[0], \%movie);
	
	&get_user($USERID, \%USER);
	if ($USER{groupAdmin}){
		$isAdmin = 'e';
	}
	
	print qq{
                <table cellspacing="0" cellpadding="1" border="0" width="100%">
	};

	$year = '';
        foreach $movieID (@movies){
                &get_movie($movieID, \%movie);
		
		$movie{date} =~ /^(....)/; # grab the year
		if ($year ne $1){
			$year = $1;
			print qq{
				<tr><th colspan="5">$year</th></tr>
			};
		}
		$sql = "SELECT DATE_FORMAT('$movie{date}', '%b %d')";
		$sth = $dbh_tnmc->prepare($sql); 
		$sth->execute();
		($dateString) = $sth->fetchrow_array();
		print qq{
			<tr>
				<td nowrap>$movie{title}</td>
				<td nowrap>$dateString</td>
				<td nowrap>&nbsp;<a href="
					javascript:window.open(
					'movie_view.cgi?movieID=$movieID',
					'ViewMovie',
					'resizable,height=350,width=450');
					index.cgi
					">v</a>
					<a href="movie_edit_admin.cgi?movieID=$movieID">$isAdmin</a></td>
			</tr>
		};
        }

	print qq{
                </table>
        };
}


##########################################################
#### The end.
##########################################################

