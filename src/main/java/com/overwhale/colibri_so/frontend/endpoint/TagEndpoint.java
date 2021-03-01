package com.overwhale.colibri_so.frontend.endpoint;

import com.overwhale.colibri_so.frontend.dto.TagDto;
import com.overwhale.colibri_so.frontend.service.TagService;
import com.vaadin.flow.server.connect.Endpoint;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.UUID;

@Endpoint
public class TagEndpoint extends CrudEndpoint<TagDto, UUID> {
  private final TagService service;

  public TagEndpoint(@Autowired TagService service) {
    this.service = service;
  }

  @Override
  protected TagService getService() {
    return service;
  }
}
