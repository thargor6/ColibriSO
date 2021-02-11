package com.overwhale.colibri_so.domain.endpoint;

import com.overwhale.colibri_so.domain.entity.SnippetProject;
import com.overwhale.colibri_so.domain.entity.SnippetTag;
import com.overwhale.colibri_so.domain.service.SnippetProjectService;
import com.overwhale.colibri_so.domain.service.SnippetTagService;
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
