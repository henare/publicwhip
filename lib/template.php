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
  public function __construct($filename, $colour_scheme = 'default')
  {
    $this->template_dir = HTML_TEMPLATES_DIRECTORY;
    parent::__construct($filename);
    $this->assign('colour_scheme', $colour_scheme);
  }
}

?>
