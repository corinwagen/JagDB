package JagDB::Controller::Question;
use Moose;
use namespace::autoclean;
use Catalyst::Plugin::Redirect;

BEGIN { extends 'Catalyst::Controller' }


#sub setup : Chained('/') PathPrefix CaptureArgs(1) {
#        my ( $self, $c, $id ) = @_;
##        my $cc = $c->model('DB::')->find( $id );
#        $c->stash->{cycle_count} = $cc;
#
#}
#
sub view_questions : Local {
    my ($self, $c, $rs) = @_; 
    my $p = $c->req->params;

    my $search; 
    my @questions = $c->model('DB::Tossup')->search_rs( $search, {pages => 1, rows => 50})->all;
    
    if ($rs) {
        @questions = @{$rs};    
    }

    $c->stash->{questions} = \@questions;
    $c->stash->{question_count} = scalar(@questions);
    
}

sub add_questions : Local {
    my ($self, $c) = @_;

}

sub process_block_import : Local {
    my ($self, $c) = @_; 
    
#    my @questions = $c->model('DB::Tossup')->search_rs( {id => '51'}, {pages => 1, rows => 50})->all;
#    my $rs = \@questions;
#
#    $c->response->redirect( $c->uri_for($c->controller->action_for('view_questions')));
my $url =  $c->uri_for($c->controller->action_for('view_questions'));
warn "url $url";
    return $c->res->redirect( $url );
    $c->detach();
}

#sub edit_question : Chained('setup') {
#    my ($self, $c) = @_; 
#
#}

1;
