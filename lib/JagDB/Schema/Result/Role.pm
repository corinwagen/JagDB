use utf8;
package JagDB::Schema::Result::Role;

use strict;
use warnings;

use Moose;
use MooseX::NonMoose;
use MooseX::MarkAsMethods autoclean => 1;
use MooseX::Method::Signatures;
use DateTime;

extends 'DBIx::Class::Core';

__PACKAGE__->load_components("InflateColumn::DateTime");
__PACKAGE__->table("roles");
__PACKAGE__->add_columns(
  "id",
  { data_type => "integer", is_nullable => 0 },
  "role",
  { data_type => "text", is_nullable => 1 },
);
__PACKAGE__->set_primary_key("id");

