package com.overwhale.colibri_so.domain.service;

import com.overwhale.colibri_so.domain.entity.Snippet;
import com.overwhale.colibri_so.domain.repository.SnippetRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.time.OffsetDateTime;
import java.util.UUID;

@Service
public class SnippetService extends CrudService<Snippet, UUID> {
  private final SnippetRepository repository;

  public SnippetService(@Autowired SnippetRepository repository) {
    this.repository = repository;
  }

  @Override
  public Snippet update(Snippet entity) {
    if (entity.getId() == null) {
      entity.setCreationTime(OffsetDateTime.now());
      entity.setId(UUID.randomUUID());
    }
    else {
      entity.setLastChangedTime(OffsetDateTime.now());
    }
    return super.update(entity);
  }

  @Override
  protected SnippetRepository getRepository() {
    return repository;
  }

  public int countForProjectId(String projectId) {
    return (int)this.getRepository().countForProjectId(UUID.fromString(projectId));
  }

  public Page<Snippet> listForProjectId(String projectId, Pageable pageable) {
    return this.getRepository().findForProjectId(UUID.fromString(projectId), pageable);
  }

}
