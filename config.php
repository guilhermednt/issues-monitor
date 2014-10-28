<?php

require_once __DIR__.'/vendor/autoload.php';

use Github\HttpClient\CachedHttpClient;
use Github\Client;

class IssueCheck
{

    private static $instance;
    private $client;

    protected function __construct($parameters)
    {
        $this->client = new Client(
            new CachedHttpClient(array('cache_dir' => '/tmp/github-api-cache'))
        );

        $apiToken = $parameters['apiToken'];
        if (strlen($apiToken)) {
            $this->client->authenticate($apiToken, null, Client::AUTH_HTTP_TOKEN);
        }
    }

    /**
     * @return Client
     */
    public function getClient()
    {
        return $this->client;
    }

    /**
     * @return IssueCheck
     */
    public static function getInstance()
    {
        if (self::$instance === null) {
            $parameters = parse_ini_file('parameters.ini');
            self::$instance = new self($parameters);
        }

        return self::$instance;
    }

}
