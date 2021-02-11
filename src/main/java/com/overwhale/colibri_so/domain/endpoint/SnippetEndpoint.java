package com.overwhale.colibri_so.domain.endpoint;

import com.overwhale.colibri_so.domain.entity.Snippet;
import com.overwhale.colibri_so.domain.service.SnippetService;
import com.vaadin.flow.server.connect.Endpoint;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.vaadin.artur.helpers.GridSorter;
import org.vaadin.artur.helpers.PagingUtil;

import java.util.List;
import java.util.UUID;

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
