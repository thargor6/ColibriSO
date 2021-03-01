package com.overwhale.colibri_so.frontend.endpoint;

import com.overwhale.colibri_so.frontend.dto.ProjectDto;
import com.overwhale.colibri_so.frontend.service.ProjectService;
import com.vaadin.flow.server.connect.Endpoint;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.UUID;

@Endpoint
public class ProjectEndpoint extends CrudEndpoint<ProjectDto, UUID> {
  private final ProjectService service;

  public ProjectEndpoint(@Autowired ProjectService service) {
    this.service = service;
  }

  @Override
  protected ProjectService getService() {
    return service;
  }
}
