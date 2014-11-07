<?php

require_once 'config.php';

use \IssueCheck;

$client = IssueCheck::getInstance()->getClient();
$maxLength = IssueCheck::getInstance()->getConfig('titleMaxLength');

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
    if (strlen($text) > $maxLength) {
        $text = substr($text, 0, $maxLength - 3) . '...';
    }
} else {
    $text = count($issues);
}

echo sprintf($template, htmlspecialchars($text), $githubLogo, htmlspecialchars(implode(PHP_EOL, $messages)));
