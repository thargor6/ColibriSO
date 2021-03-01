package com.overwhale.colibri_so.frontend.endpoint;

import com.overwhale.colibri_so.frontend.dto.SnippetProjectDto;
import com.overwhale.colibri_so.frontend.service.SnippetProjectService;
import com.vaadin.flow.server.connect.Endpoint;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.UUID;

@Endpoint
public class SnippetProjectEndpoint extends CrudEndpoint<SnippetProjectDto, UUID> {
  private final SnippetProjectService service;

  public SnippetProjectEndpoint(@Autowired SnippetProjectService service) {
    this.service = service;
  }

  @Override
  protected SnippetProjectService getService() {
    return service;
  }
}
