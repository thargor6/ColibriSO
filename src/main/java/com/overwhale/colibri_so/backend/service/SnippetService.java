package com.overwhale.colibri_so.backend.service;

import com.overwhale.colibri_so.backend.entity.Intent;
import com.overwhale.colibri_so.backend.entity.Project;
import com.overwhale.colibri_so.backend.entity.Snippet;
import com.overwhale.colibri_so.backend.entity.Tag;
import com.overwhale.colibri_so.backend.repository.SnippetIntentRepository;
import com.overwhale.colibri_so.backend.repository.SnippetProjectRepository;
import com.overwhale.colibri_so.backend.repository.SnippetRepository;
import com.overwhale.colibri_so.backend.repository.SnippetTagRepository;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.time.OffsetDateTime;
import java.util.UUID;

@Service
public class SnippetService extends CrudService<Snippet, UUID> {
  private final SnippetRepository repository;
  private final SnippetTagRepository tagRepository;
  private final SnippetIntentRepository intentRepository;
  private final SnippetProjectRepository projectRepository;

  public SnippetService(SnippetRepository repository, SnippetTagRepository tagRepository, SnippetIntentRepository intentRepository, SnippetProjectRepository projectRepository) {
    this.repository = repository;
    this.tagRepository = tagRepository;
    this.intentRepository = intentRepository;
    this.projectRepository = projectRepository;
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

  public Page<Intent> listIntentsForSnippetId(String snippetId, Pageable pageable) {
    return this.getRepository().findIntentsForSnippet(UUID.fromString(snippetId), pageable);
  }

  public Page<Tag> listTagsForSnippetId(String snippetId, Pageable pageable) {
    return this.getRepository().findTagsForSnippet(UUID.fromString(snippetId), pageable);
  }

  public Page<Project> listProjectsForSnippetId(String snippetId, Pageable pageable) {
    return this.getRepository().findProjectsForSnippet(UUID.fromString(snippetId), pageable);
  }

  @Override
  public void delete(UUID uuid) {
    super.delete(uuid);
    tagRepository.deleteBySnippetId(uuid);
    projectRepository.deleteBySnippetId(uuid);
    intentRepository.deleteBySnippetId(uuid);
  }
}
