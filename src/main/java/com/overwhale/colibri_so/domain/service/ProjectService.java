package com.overwhale.colibri_so.domain.service;

import com.overwhale.colibri_so.domain.entity.Project;
import com.overwhale.colibri_so.domain.repository.ProjectRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.time.OffsetDateTime;
import java.util.UUID;

@Service
public class ProjectService extends CrudService<Project, UUID> {
  private final ProjectRepository repository;

  public ProjectService(@Autowired ProjectRepository repository) {
    this.repository = repository;
  }

  @Override
  public Project update(Project entity) {
    if (entity.getId() == null) {
      entity.setCreationTime(OffsetDateTime.now());
      entity.setId(UUID.randomUUID());
      // TODO
      entity.setCreatorId(UUID.randomUUID());
    }
    entity.setLastChangedTime(OffsetDateTime.now());
    return super.update(entity);
  }

  @Override
  protected ProjectRepository getRepository() {
    return repository;
  }
}
