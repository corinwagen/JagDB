package JagDB::Controller::Question;
use Moose;
use namespace::autoclean;

BEGIN { extends 'Catalyst::Controller' }

sub view_questions : Local {
    my ($self, $c) = @_; 

    my $search; 

    my @questions = $c->model('DB::Tossup')->search_rs( $search, {pages => 1, rows => 50})->all;
    $c->stash->{questions} = \@questions;
    $c->stash->{question_count} = scalar(@questions);
    
}

sub add_questions : Local {
    my ($self, $c) = @_;

}

1;
