package tnmc::util::date;

use strict;

#use Time::Local;

sub format_date{
    my ($format, $date) = @_;
    
    return 'never' if !$date;

    $date =~ /(....)(..)(..)(..)(..)(..)/;
    my ($yyyy, $mm, $dd, $h, $m, $s, @date);
    $yyyy = $1;
    $mm = $2;
    $dd = $3;
    $h = $4;
    $m = $5;
    $s = $6;
    @date = ($1, $2, $3, $4, $5, $6);
    if ($format eq 'numeric'){
        return sprintf("%s/%s/%s %s:%s:%s", @date);
        
    }
    
}

return 1;

#### Other Subs from LANGSERVER



sub old_format_date {
    my ($timestamp) = @_;

    return 'Not Available' if (! defined $timestamp);

    my ($year, $month, $day, 
        $hour, $min, $sec) = &convert_date($timestamp);

    my $mon = ('', 'January', 'February', 'March', 'April', 'May', 
               'June', 'July', 'August', 'September', 'October', 
               'November', 'December')[$month];

    return sprintf("%s %d, %d %02d:%02d:%02d", $mon, $day, $year, $hour, $min, $sec);
}

sub format_date_fname {
    my ($timestamp) = @_;

    $timestamp = time() if (! defined $timestamp);
    my ($year, $month, $day, 
        $hour, $min, $sec) = &convert_date($timestamp);

    my $mon = ('', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
               'Aug', 'Sep', 'Oct', 'Nov', 'Dec')[$month];

    return  "$mon$day";
}

# This converts either a Unix timestamp (number of seconds after 1970)
# or a mySQL timestamp (YYYYMMDDHHMMSS) to a date array in the order
# year, month, day, hour, minute, second
sub convert_date {
    my ($timestamp) = @_;

    return if (! defined $timestamp);

    my ($year, $month, $day, 
        $hour, $min, $sec) = unpack("a4a2a2a2a2a2", $timestamp);

    if ($sec eq '' || $min eq '' || $hour eq '' ||
        $day eq '' || $month eq '' || $year eq '') {
        ($sec, $min, $hour, 
         $day, $month, $year) = (localtime($timestamp))[0, 1, 2, 3, 4, 5];

        $month = $month + 1;
        $year = $year + 1900;
    }

    return ($year, $month, $day, $hour, $min, $sec);
}

sub convert_to_epoch {
    my ($timestamp) = @_;

    return 0 if (! defined $timestamp);

    my ($year, $month, $day, 
        $hour, $min, $sec) = unpack("a4a2a2a2a2a2", $timestamp);

    return timelocal($sec, $min, $hour, $day, $month-1, $year-1900);     
}
    
1;