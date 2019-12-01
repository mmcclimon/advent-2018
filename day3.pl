#!perl
use warnings;
use v5.24;

my @data = (
  '#1 @ 1,3: 4x4',
  '#2 @ 3,1: 4x4',
  '#3 @ 5,5: 2x2',
);

open my $fh, '<', 'd3.txt' or die "couldn't read file: $!";
@data = map {; chomp; $_ } <$fh>;

my $matrix = [ [], [] ];
my $total = 0;

for my $d (@data) {
  my ($id, $x_start, $y_start, $width, $height) = $d =~ /#(\d+) \@ (\d+),(\d+): (\d+)x(\d+)/;

  for my $x ($x_start .. $x_start + $width - 1) {
    for my $y ($y_start .. $y_start + $height - 1) {
      my $there = $matrix->[$y][$x];
      $total++ if defined $there && $there eq '1';
      $matrix->[$y][$x] = $there ? 'X' : 1;
    }
  }
}

say "total: $total";

# Hard part

ID: for my $d (@data) {
  my ($id, $x_start, $y_start, $width, $height) = $d =~ /#(\d+) \@ (\d+),(\d+): (\d+)x(\d+)/;

  for my $x ($x_start .. $x_start + $width - 1) {
    for my $y ($y_start .. $y_start + $height - 1) {
      next ID if $matrix->[$y][$x] eq 'X';
    }
  }

  say "found one: $id";
  last ID;
}
