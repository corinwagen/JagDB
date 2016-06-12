package JagDB::Schema::ResultSet::Bonus;

use Moose; 
use MooseX::Method::Signatures;
use DateTime;

BEGIN { extends 'DBIx::Class::ResultSet'; }

method create_bonus (:$user!, :$params!) {
    $user ? 1 : die "Can't create bonus without user id!";

    my $new_bonus = $self->create({
        created_by_id   => $user->id || '',
        created_on      => DateTime->now(time_zone => 'local'),
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
