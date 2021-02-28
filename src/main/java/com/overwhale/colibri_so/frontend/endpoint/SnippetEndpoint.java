package com.overwhale.colibri_so.frontend.endpoint;

import com.overwhale.colibri_so.backend.service.SnippetService;
import com.vaadin.flow.server.connect.Endpoint;
import org.springframework.beans.factory.annotation.Autowired;

@Endpoint
public class SnippetEndpoint extends SnippetCrudEndpoint {
  private final SnippetService service;

  public SnippetEndpoint(@Autowired SnippetService service) {
    this.service = service;
  }

  @Override
  protected SnippetService getService() {
    return service;
  }

}
