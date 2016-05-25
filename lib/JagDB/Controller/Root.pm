package JagDB::Controller::Root;
use Moose;
use namespace::autoclean;

BEGIN { extends 'Catalyst::Controller' }

__PACKAGE__->config(namespace => '');

sub index :Path :Args(0) {
    my ( $self, $c ) = @_;
    $c->stash->{title => "Home"};
#    $c->stash->{wrapper => "src/wrapper.tt"};
}

sub default :Path {
    my ( $self, $c ) = @_;
    $c->response->status(404);
}

sub end : ActionClass('RenderView') {
    my ($self, $c) = @_; 
    
    $c->forward('JagDB::View::HTML');    
    
}


__PACKAGE__->meta->make_immutable;

1;
