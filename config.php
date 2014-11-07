<?php

require_once __DIR__ . '/vendor/autoload.php';

use Github\HttpClient\CachedHttpClient;
use Github\Client;

class IssueCheck
{

    private static $instance;
    private $client;
    private $config;

    protected function __construct($parameters)
    {
        $this->client = new Client(
            new CachedHttpClient(array('cache_dir' => '/tmp/github-api-cache'))
        );

        $apiToken = $parameters['apiToken'];
        if (strlen($apiToken) > 0) {
            $this->client->authenticate($apiToken, null, Client::AUTH_HTTP_TOKEN);
        }
        unset($parameters['apiToken']);
        $this->setConfig($parameters);
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
            $paramsFile = __DIR__ . DIRECTORY_SEPARATOR . 'parameters.ini';
            if (file_exists($paramsFile)) {
                $parameters = parse_ini_file($paramsFile);
            } else {
                $dir = __DIR__;
                die("parameters.ini not found in $dir!");
            }
            self::$instance = new self($parameters);
        }

        return self::$instance;
    }

    public function getConfig($key)
    {
        return $this->config[$key];
    }

    private function setConfig($config)
    {
        $this->config = $config;
        return $this;
    }

}
