#!/usr/bin/perl

##################################################################
#	Jeff Steinbok - steinbok@interchange.ubc.ca
##################################################################
### Opening Stuff. Modules and all that. nothin' much interesting.

use DBI;
use CGI;

use lib '/usr/local/apache/tnmc/';
use tnmc;

	#############
	### Main logic
	
	$cgih = new CGI;
	
	&db_connect();
	&get_cookie();

	$sql = "SELECT NOW()";
	$sth = $dbh_tnmc->prepare($sql);
	$sth->execute();
	($time) = $sth->fetchrow_array();

	my $newSuggestion  =  $cgih->param(suggestion);
        
	$oldSuggestions =  &get_general_config("suggestions");

	my $SUGG = 
		  $oldSuggestions
		. "\n"
		. "$USERID{username} $USERID - $time \n"
		. "====================================\n"
		. $newSuggestion . "\n";

	&set_general_config('suggestions', $SUGG);

	require 'broadcast/BROADCAST.pl';
	&smsShout('1', "IDEA: $newSuggestion");

	&db_disconnect();

	print "Location: http://tnmc.dhs.org/\n\n";
