package JagDB::Schema::ResultSet::Tossup;

use Moose; 
use MooseX::Method::Signatures;
use DateTime;

BEGIN { extends 'DBIx::Class::ResultSet'; }

method create_tossup (:$user!, :$params!) {
    $user ? 1 : die "Can't create tossup without user id!";

    my $new_tossup = $self->create({
        created_by_id   => $user->id || '',
        created_on      => DateTime->now(time_zone => 'local'),
        packet_id       => $params->{packet_id} || '',
        subject_id      => $params->{subject_id} || '',
        question        => $params->{question} || '',
        answer          => $params->{answer} || '',
    });

    return $new_tossup;
}

1;
