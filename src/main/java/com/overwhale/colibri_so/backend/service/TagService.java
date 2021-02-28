package com.overwhale.colibri_so.backend.service;

import com.overwhale.colibri_so.backend.entity.Tag;
import com.overwhale.colibri_so.backend.repository.TagRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.time.OffsetDateTime;
import java.util.UUID;

@Service
public class TagService extends CrudService<Tag, UUID> {
  private final TagRepository repository;

  public TagService(@Autowired TagRepository repository) {
    this.repository = repository;
  }

  @Override
  public Tag update(Tag entity) {
    if (entity.getId() == null) {
      entity.setCreationTime(OffsetDateTime.now());
      entity.setId(UUID.randomUUID());
    } else {
      entity.setLastChangedTime(OffsetDateTime.now());
    }
    return super.update(entity);
  }

  @Override
  protected TagRepository getRepository() {
    return repository;
  }
}
