package com.overwhale.colibri_so.frontend.endpoint;

import com.overwhale.colibri_so.frontend.mapper.IntentMapper;
import com.overwhale.colibri_so.frontend.mapper.ProjectMapper;
import com.overwhale.colibri_so.frontend.mapper.SnippetMapper;
import com.overwhale.colibri_so.frontend.mapper.TagMapper;
import com.overwhale.colibri_so.frontend.service.SnippetService;
import com.vaadin.flow.server.connect.Endpoint;

@Endpoint
public class SnippetEndpoint extends SnippetCrudEndpoint {
  private final SnippetService service;

  public SnippetEndpoint(
      SnippetService service,
      IntentMapper intentMapper,
      SnippetMapper snippetMapper,
      ProjectMapper projectMapper,
      TagMapper tagMapper) {
    super(intentMapper, snippetMapper, projectMapper, tagMapper);
    this.service = service;
  }

  @Override
  protected SnippetService getService() {
    return service;
  }
}
