<?php

require_once 'config.php';

use \IssueCheck;

$client = IssueCheck::getInstance()->getClient();

$currentUser = $client->currentUser()->show();
$username = $currentUser['login'];

$filter = array('assignee' => $username, 'state' => 'open');
$issues = $client->issues()->all('PROCERGS', 'login-cidadao', $filter);

$title = "Your issues:";
$messages = array();
foreach ($issues as $issue) {
    $messages[] = sprintf('[#%s] %s', $issue['number'], $issue['title']);
}

if (count($messages) > 3) {
    $body = array();
    $other = 0;
    foreach ($messages as $message) {
        if (count($body) === 2) {
            $other += 1;
            continue;
        }
        $body[] = $message;
    }
    if (count($body) === 2) {
        $body[] = sprintf("And %d other issues.", $other);
    }
} else {
    $body = $messages;
}

$githubLogo = realpath(__DIR__ . '/images/GitHub-Mark-Light-120px-plus.png');
$command = sprintf('notify-send --icon="%s" "%s" "%s"', $githubLogo, $title,
                   implode(PHP_EOL, $body));
system($command);
