use utf8;
package JagDB::Schema::Result::Tossup;

use strict;
use warnings;

use Moose;
use MooseX::NonMoose;
use MooseX::MarkAsMethods autoclean => 1;
use MooseX::Method::Signatures;
use DateTime;

extends 'DBIx::Class::Core';

__PACKAGE__->load_components("InflateColumn::DateTime");
__PACKAGE__->table("tossups");
__PACKAGE__->add_columns(
  "id",
  { data_type => "integer", is_nullable => 0 },
  "question",
  { data_type => "text", is_nullable => 1 },
  "answer",
  { data_type => "text", is_nullable => 1 },
  "flagged",
  { data_type => "char", is_nullable => 1, size => 1 },
  "created_at",
  {
    data_type => "datetime",
    datetime_undef_if_invalid => 1,
    is_nullable => 1,
  },
  "updated_at",
  {
    data_type => "datetime",
    datetime_undef_if_invalid => 1,
    is_nullable => 1,
  },
  "packet_id",
  { data_type => "integer", is_nullable => 1 },
  "subject_id",
  { data_type => "integer", is_nullable => 1 },
  "tossup_text",
  { data_type => "text", is_nullable => 1 },
);
__PACKAGE__->set_primary_key("id");
#__PACKAGE__->meta->make_immutable;

method update_tossup (:$user!, :$params!) {
    $user ? 1 : die "Can't update tossup without user id!";

    my $new_tossup = $self->update({
        updated_by_id   => $user->id || '',
        updated_on      => DateTime->now(time_zone => 'local'),
        packet_id       => $params->{packet_id} || '',
        subject_id      => $params->{subject_id} || '',
        question        => $params->{question} || '',
        answer          => $params->{answer} || '',
    });

    return $new_tossup;
}


1;
