#!/usr/bin/perl

##################################################################
#	Scott Thompson
##################################################################
### Opening Stuff. Modules and all that. nothin' much interesting.

use lib '/tnmc';

use tnmc::security::auth;
use tnmc::db;
use tnmc::template;

require 'fieldtrip/FIELDTRIP.pl';

{
	#############
	### Main logic

	&db_connect();
	&header();

	%trip;	
	$cgih = new CGI;
	$tripID = $cgih->param('tripID');
	$CONFIRM = $cgih->param('CONFIRM');
	
       	&get_trip($tripID, \%trip);

        if (!$tripID){
            ### Bad tripID
            print qq{
                <b>Hey!</b><br>
                No trip ID!!
            };
        }
        if ($trip{AdminUserID} != $USERID){
            ### Bad userID
            print qq{
                <b>Hey!</b><br>
                You're not allowed to do this!! <!-- ' -->
            };
        }
        else{

            if (!$CONFIRM){
                ### Ask for confirmation
                print qq {
                    <form action="trip_del.cgi" method="post">
                    <input type="hidden" name="tripID" value="$tripID">
                    <b>Are you SURE that you want to permanently delete this trip?</b>
                    <p>
                    $trip{title} ($tripID)
                    <p>
                    <input type="checkbox" name="CONFIRM" value="1">Yes
                    <p>
                    <input type="submit" value="Delete this Trip">
                    </form>

                };
            }else{
                ### Delete the trip

                print qq{
                    <b>Trip Deleted:</b>
                    <p>
                    $trip{title} ($tripID)
                };
                
                $sql = "DELETE FROM FieldtripSurvey WHERE tripID = $tripID";
                $sth = $dbh_tnmc->prepare($sql);
                $sth->execute();

                &del_trip($tripID);

                print qq{
                    <p>
                    <a href="index.cgi">Continue</a>
                };
            }
        }
	
	&footer();

	&db_disconnect();
}