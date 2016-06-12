use utf8;
package JagDB::Schema::Result::Bonus;

use strict;
use warnings;

use Moose;
use MooseX::NonMoose;
use MooseX::MarkAsMethods autoclean => 1;
use MooseX::Method::Signatures;
use DateTime;
extends 'DBIx::Class::Core';

__PACKAGE__->load_components("InflateColumn::DateTime");

__PACKAGE__->table("bonuses");
__PACKAGE__->add_columns(
  "id",
  { data_type => "integer", is_nullable => 0 },
  "leadin",
  { data_type => "text", is_nullable => 1 },
  "part1",
  { data_type => "text", is_nullable => 1 },
  "answer1",
  { data_type => "text", is_nullable => 1 },
  "part2",
  { data_type => "text", is_nullable => 1 },
  "answer2",
  { data_type => "text", is_nullable => 1 },
  "part3",
  { data_type => "text", is_nullable => 1 },
  "answer3",
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
  "bonus_text",
  { data_type => "text", is_nullable => 1 },
);
__PACKAGE__->set_primary_key("id");
#__PACKAGE__->meta->make_immutable;

method update_bonus (:$user!, :$params!) {
    $user ? 1 : die "Can't update bonus without user id!";

    my $new_bonus = $self->update({
        updated_by_id   => $user->id || '',
        updated_on      => DateTime->now(time_zone => 'local'),
        packet_id       => $params->{packet_id} || '',
        subject_id      => $params->{subject_id} || '',
        leadin          => $params->{leadin} || '',
        part1           => $params->{part1} || '',
        answer1         => $params->{answer1} || '',
        part2           => $params->{part2} || '',
        answer2         => $params->{answer2} || '',
        part3           => $params->{part3} || '',
        answer3         => $params->{answer3} || '',
    });
    return $new_bonus;
}





1;
