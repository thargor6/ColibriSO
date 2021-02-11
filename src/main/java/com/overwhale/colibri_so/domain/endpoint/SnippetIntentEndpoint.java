package com.overwhale.colibri_so.domain.endpoint;

import com.overwhale.colibri_so.domain.entity.SnippetIntent;
import com.overwhale.colibri_so.domain.entity.SnippetTag;
import com.overwhale.colibri_so.domain.service.SnippetIntentService;
import com.overwhale.colibri_so.domain.service.SnippetTagService;
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
