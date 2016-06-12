use utf8;
package JagDB::Schema::Result::Tournament;

# Created by DBIx::Class::Schema::Loader
# DO NOT MODIFY THE FIRST PART OF THIS FILE

=head1 NAME

JagDB::Schema::Result::Tournament

=cut

use strict;
use warnings;

use Moose;
use MooseX::NonMoose;
use MooseX::MarkAsMethods autoclean => 1;
extends 'DBIx::Class::Core';

=head1 COMPONENTS LOADED

=over 4

=item * L<DBIx::Class::InflateColumn::DateTime>

=back

=cut

__PACKAGE__->load_components("InflateColumn::DateTime");

=head1 TABLE: C<tournaments>

=cut

__PACKAGE__->table("tournaments");

=head1 ACCESSORS

=head2 id

  data_type: 'integer'
  is_nullable: 0

=head2 name

  data_type: 'char'
  is_nullable: 1
  size: 40

=head2 difficulty

  data_type: 'integer'
  is_nullable: 1

=head2 power

  data_type: 'char'
  is_nullable: 1
  size: 1

=head2 year

  data_type: 'integer'
  is_nullable: 1

=head2 tournament_mongo

  data_type: 'text'
  is_nullable: 1

=cut

__PACKAGE__->add_columns(
  "id",
  { data_type => "integer", is_nullable => 0 },
  "name",
  { data_type => "char", is_nullable => 1, size => 40 },
  "difficulty",
  { data_type => "integer", is_nullable => 1 },
  "power",
  { data_type => "char", is_nullable => 1, size => 1 },
  "year",
  { data_type => "integer", is_nullable => 1 },
  "tournament_mongo",
  { data_type => "text", is_nullable => 1 },
);

=head1 PRIMARY KEY

=over 4

=item * L</id>

=back

=cut

__PACKAGE__->set_primary_key("id");


# Created by DBIx::Class::Schema::Loader v0.07045 @ 2016-05-25 10:41:01
# DO NOT MODIFY THIS OR ANYTHING ABOVE! md5sum:0K7WxQRe2fmGvxnMLwYaoA


# You can replace this text with custom code or comments, and it will be preserved on regeneration
__PACKAGE__->meta->make_immutable;
1;
