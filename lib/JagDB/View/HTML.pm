package JagDB::View::HTML;
use Moose;
use namespace::autoclean;

extends 'Catalyst::View::TT';

__PACKAGE__->config(
    TEMPLATE_EXTENSION => '.tt',
    INCLUDE_PATH => [
        JagDB->path_to( 'root', 'src' ),
    ],
    TIMER => 0,
    WRAPPER => "wrapper.tt",
);

=head1 NAME

JagDB::View::HTML - TT View for JagDB

=head1 DESCRIPTION

TT View for JagDB.

=head1 SEE ALSO

L<JagDB>

=head1 AUTHOR

Corin Wagen

=head1 LICENSE

This library is free software. You can redistribute it and/or modify
it under the same terms as Perl itself.

=cut

1;
