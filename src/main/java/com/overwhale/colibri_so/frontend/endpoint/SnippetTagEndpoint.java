package com.overwhale.colibri_so.frontend.endpoint;

import com.overwhale.colibri_so.backend.entity.SnippetTag;
import com.overwhale.colibri_so.backend.service.SnippetTagService;
import com.vaadin.flow.server.connect.Endpoint;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.UUID;

@Endpoint
public class SnippetTagEndpoint extends CrudEndpoint<SnippetTag, UUID> {
  private final SnippetTagService service;

  public SnippetTagEndpoint(@Autowired SnippetTagService service) {
    this.service = service;
  }

  @Override
  protected SnippetTagService getService() {
    return service;
  }
}
