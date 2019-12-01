#!perl
use v5.24;
use warnings;
use Data::Dumper::Concise;
use List::Util qw(max sum first);

open my $fh, '<', 'd4.txt' or die "Can't open file: $!";
my @data = <$fh>;

@data = map  { $_->[0] }
        sort { $a->[1] cmp $b->[1]  }
        map  { chomp; my ($d) = /^\[(.*?)\]/; [ $_, $d ] } @data;

my $guards;
my @naps;
my $this_guard;
my $asleep;

for my $line (@data) {
  my ($time, $rest) = $line =~ /^\[[-0-9]+ ([0-9:]+)\] (.*)/;

  my (undef, $min) = split ':', $time;

  if (my ($guard) = $rest =~ /Guard #(\d+) begins shift/) {
    $this_guard = $guard;
  } elsif ($rest eq 'falls asleep') {
    $asleep = 0+ $min;
  } elsif ($rest eq 'wakes up') {

    for my $this_min ($asleep .. $min-1) {
      $guards->{$this_guard}{$this_min} //= 0;
      $guards->{$this_guard}{$this_min}++;
    }

    undef($asleep);

  } else {
    die "weird line: $line";
  }
}

for my $guard (keys %$guards) {
  my $total = sum(values $guards->{$guard}->%*);
  my $max   = max(values $guards->{$guard}->%*);
  my $key   = first { $guards->{$guard}{$_} == $max } keys $guards->{$guard}->%*;

  $guards->{$guard} = {
    total         => $total,
    target_minute => $key,
    asleep_count  => $max,
  };
}

my ($pick) = map  { $_->[0] }
             sort { $b->[1] <=> $a->[1]  }
             map  { [ $_, $guards->{$_}{total} ] } keys %$guards;

say "easy:";
say "  $pick: total=$guards->{$pick}{total}, min=$guards->{$pick}{target_minute}";
say "  " . $pick * $guards->{$pick}{target_minute};

my ($hpick) = map  { $_->[0] }
              sort { $b->[1] <=> $a->[1]  }
              map  { [ $_, $guards->{$_}{asleep_count}] } keys %$guards;

say "hard";
say "  $hpick: total=$guards->{$hpick}{total}, min=$guards->{$hpick}{target_minute}";
say "  " . $hpick * $guards->{$hpick}{target_minute};
