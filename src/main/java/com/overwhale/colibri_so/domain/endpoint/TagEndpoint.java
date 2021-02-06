package com.overwhale.colibri_so.domain.endpoint;

import com.overwhale.colibri_so.domain.entity.Tag;
import com.overwhale.colibri_so.domain.service.TagService;
import com.vaadin.flow.server.connect.Endpoint;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.UUID;

@Endpoint
public class TagEndpoint extends CrudEndpoint<Tag, UUID> {
  private final TagService service;

  public TagEndpoint(@Autowired TagService service) {
    this.service = service;
  }

  @Override
  protected TagService getService() {
    return service;
  }
}
