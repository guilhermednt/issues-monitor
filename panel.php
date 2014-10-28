<?php

require_once 'config.php';

use \IssueCheck;

$client = IssueCheck::getInstance()->getClient();

$currentUser = $client->currentUser()->show();
$username = $currentUser['login'];

$filter = array('assignee' => $username, 'state' => 'open');
$issues = $client->issues()->all('PROCERGS', 'login-cidadao', $filter);

$messages = array();
foreach ($issues as $issue) {
    $messages[] = sprintf('[#%s] %s', $issue['number'], $issue['title']);
}

$githubLogo = realpath(__DIR__ . '/images/github.icon.png');
$template = ''
    . '<txt> %s</txt>'
    . '<img>%s</img>'
    . '<tool>%s</tool>';

if (count($issues) === 1) {
    $text = reset($messages);
    if (strlen($text) > 30) {
        $text = substr($text, 0, 27) . '...';
    }
} else {
    $text = count($issues);
}

echo sprintf($template, $text, $githubLogo, implode(PHP_EOL, $messages));
