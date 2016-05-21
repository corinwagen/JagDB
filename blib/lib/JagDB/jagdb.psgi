use strict;
use warnings;

use JagDB;

my $app = JagDB->apply_default_middlewares(JagDB->psgi_app);
$app;

