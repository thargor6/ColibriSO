package com.overwhale.colibri_so.domain.service;


import com.overwhale.colibri_so.domain.entity.SnippetProject;
import com.overwhale.colibri_so.domain.repository.SnippetProjectRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.time.OffsetDateTime;
import java.util.UUID;

@Service
public class SnippetProjectService extends CrudService<SnippetProject, UUID> {
  private final SnippetProjectRepository repository;

  public SnippetProjectService(@Autowired SnippetProjectRepository repository) {
    this.repository = repository;
  }

  @Override
  protected SnippetProjectRepository getRepository() {
    return repository;
  }
}
