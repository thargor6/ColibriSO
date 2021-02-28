package com.overwhale.colibri_so.frontend.endpoint;

import com.overwhale.colibri_so.backend.entity.SnippetIntent;
import com.overwhale.colibri_so.backend.service.SnippetIntentService;
import com.vaadin.flow.server.connect.Endpoint;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.UUID;

@Endpoint
public class SnippetIntentEndpoint extends CrudEndpoint<SnippetIntent, UUID> {
  private final SnippetIntentService service;

  public SnippetIntentEndpoint(@Autowired SnippetIntentService service) {
    this.service = service;
  }

  @Override
  protected SnippetIntentService getService() {
    return service;
  }
}
