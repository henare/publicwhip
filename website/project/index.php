<?php require_once "../common.inc";
# $Id: index.php,v 1.11 2009/06/08 00:56:09 publicwhip Exp $

# The Public Whip, Copyright (C) 2003 Francis Irving and Julian Todd
# This is free software, and you are welcome to redistribute it under
# certain conditions.  However, it comes with ABSOLUTELY NO WARRANTY.
# For details see the file LICENSE.html in the top level of the source.

$template = new PW_Template_HTML('project/index.html');
$template->display();

?>
