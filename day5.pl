#!perl
use warnings;
use v5.26;

my $s = 'dabAcCaCBAcCcaDA';
open my $fh, '<', 'd5.txt';
# { local $/ = undef; $s = <$fh> }

my @chars = split //, $s;
my @chars2 = ($chars[0]);

for my $i (1..$#chars) {
  my $this_c = $chars[$i];
  my $prev_c = $chars[$i-1];

  if $this_c eq uc $prev_c

}
