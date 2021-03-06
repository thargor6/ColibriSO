package com.overwhale.colibri_so.frontend.service;

import com.overwhale.colibri_so.backend.entity.Intent;
import com.overwhale.colibri_so.backend.entity.Project;
import com.overwhale.colibri_so.backend.entity.Snippet;
import com.overwhale.colibri_so.backend.entity.Tag;
import com.overwhale.colibri_so.backend.repository.SnippetIntentRepository;
import com.overwhale.colibri_so.backend.repository.SnippetProjectRepository;
import com.overwhale.colibri_so.backend.repository.SnippetRepository;
import com.overwhale.colibri_so.backend.repository.SnippetTagRepository;
import com.overwhale.colibri_so.frontend.dto.SnippetDto;
import com.overwhale.colibri_so.frontend.mapper.SnippetMapper;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Service;
import org.vaadin.artur.helpers.CrudService;

import java.time.OffsetDateTime;
import java.util.Optional;
import java.util.UUID;

@Service
public class SnippetService extends CrudService<SnippetDto, UUID> {
  private final SnippetRepository repository;
  private final SnippetTagRepository tagRepository;
  private final SnippetIntentRepository intentRepository;
  private final SnippetProjectRepository projectRepository;
  private final SnippetMapper snippetMapper;

  public SnippetService(
      SnippetRepository repository,
      SnippetTagRepository tagRepository,
      SnippetIntentRepository intentRepository,
      SnippetProjectRepository projectRepository,
      SnippetMapper snippetMapper) {
    this.repository = repository;
    this.tagRepository = tagRepository;
    this.intentRepository = intentRepository;
    this.projectRepository = projectRepository;
    this.snippetMapper = snippetMapper;
  }

  public SnippetDto update(SnippetDto dto) {
    Snippet entity = snippetMapper.dtoToEntiy(dto);
    if (entity.getId() == null) {
      entity.setCreationTime(OffsetDateTime.now());
      entity.setId(UUID.randomUUID());
    } else {
      entity.setLastChangedTime(OffsetDateTime.now());
    }
    return snippetMapper.entityToDto(repository.save(entity));
  }

  @Override
  protected JpaRepository<SnippetDto, UUID> getRepository() {
    return null;
  }

  public Optional<SnippetDto> get(UUID id) {
    return repository.findById(id).map(e -> snippetMapper.entityToDto(e));
  }

  public void delete(UUID id) {
    repository.deleteById(id);
    tagRepository.deleteBySnippetId(id);
    projectRepository.deleteBySnippetId(id);
    intentRepository.deleteBySnippetId(id);
  }

  public Page<SnippetDto> list(Pageable pageable) {
    return repository.findAll(pageable).map(e -> snippetMapper.entityToDto(e));
  }

  public int count() {
    return (int) repository.count();
  }

  public int countForProjectId(String projectId) {
    return (int) repository.countForProjectId(UUID.fromString(projectId));
  }

  public Page<Snippet> listForProjectId(String projectId, Pageable pageable) {
    return repository.findForProjectId(UUID.fromString(projectId), pageable);
  }

  public Page<Intent> listIntentsForSnippetId(String snippetId, Pageable pageable) {
    return repository.findIntentsForSnippet(UUID.fromString(snippetId), pageable);
  }

  public Page<Tag> listTagsForSnippetId(String snippetId, Pageable pageable) {
    return repository.findTagsForSnippet(UUID.fromString(snippetId), pageable);
  }

  public Page<Project> listProjectsForSnippetId(String snippetId, Pageable pageable) {
    return repository.findProjectsForSnippet(UUID.fromString(snippetId), pageable);
  }
}
