<?php

require_once 'Twig/Autoloader.php';

Twig_Autoloader::register();

/**
 * Base class for Public Whip templates.
 * Extend this class to provide a particular output type - e.g. HTML.
 */
abstract class PW_Template
{
  protected $loader;
  protected $twig;
  protected $template;
  protected $template_dir;
  protected $data;
  
  public function __construct($filename)
  {
    $this->loader = new Twig_Loader_Filesystem($this->template_dir);
    $this->twig = new Twig_Environment($this->loader);
    $this->template = $this->twig->loadTemplate($filename);
    
    $this->data = array();
  }
  
  public function assign($key, $value)
  {
    $this->data[$key] = $value;
  }
  
  public function display()
  {
    $this->template->display($this->data);
  }
}

class PW_Template_HTML extends PW_Template
{
  private $request;
  private $user;
  
  public function __construct($filename, $colour_scheme = 'default')
  {
    $this->template_dir = HTML_TEMPLATES_DIRECTORY;
    parent::__construct($filename);
    $this->assign('colour_scheme', $colour_scheme);
    
    // Obtain request data
    $this->request = array();
    $this->request['request_uri'] = isset($_SERVER['REQUEST_URI']) ? $_SERVER['REQUEST_URI'] : '';
    
    $this->assign('request', $this->request);
    
    // Get user data
    $this->user = array();
    $this->user['logged_in'] = user_isloggedin();
    
    if ($this->user['logged_in'])
    {
      $this->user['name'] = user_getname();
    }
    
    $this->assign('user', $this->user);
  }
}

?>
