package com.overwhale.colibri_so.domain.endpoint;

import com.overwhale.colibri_so.domain.entity.Snippet;
import com.overwhale.colibri_so.domain.entity.SnippetProject;
import com.overwhale.colibri_so.domain.service.SnippetProjectService;
import com.overwhale.colibri_so.domain.service.SnippetService;
import com.vaadin.flow.server.connect.Endpoint;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.UUID;

@Endpoint
public class SnippetProjectEndpoint extends CrudEndpoint<SnippetProject, UUID> {
  private final SnippetProjectService service;

  public SnippetProjectEndpoint(@Autowired SnippetProjectService service) {
    this.service = service;
  }

  @Override
  protected SnippetProjectService getService() {
    return service;
  }
}
