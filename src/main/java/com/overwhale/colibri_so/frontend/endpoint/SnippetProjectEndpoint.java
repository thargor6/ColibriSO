package com.overwhale.colibri_so.frontend.endpoint;

import com.overwhale.colibri_so.backend.entity.SnippetProject;
import com.overwhale.colibri_so.backend.service.SnippetProjectService;
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
