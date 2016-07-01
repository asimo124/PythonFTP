#!/usr/bin/perl

use strict;
use warnings;
use diagnostics;

my $reviewer = "alex";
my $review = qq{$reviewer wrote "This book is wonderful"} . "\n";

my $editor = "steve";

$review = qq{
Dear $editor,

I really liked the subtitle that you rejected and beg you to recondisder.
It was brilliant and perfectly conveyed the tone of this book.

	"Get a job"

Sincereley,
Ovid
};

$review = <<"END"; 

Dear $editor, I'm very sorry for mocking you in the last email. Can I still get paid?

Sincerely,
Ovid
END

print $review;



